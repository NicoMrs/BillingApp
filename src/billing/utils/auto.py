from billing.utils.setup_logger import logger
from datetime import date, timedelta
from babel.dates import format_date
from billing.database import *
from ..invoice import *
from ..database.exceptions import *
from .paths import DataDir
import os

def manage_invoice():
    """
    Connect to the invoice database and generate a valid invoice.

    Workflow:
        1. Generate a new invoice.
        2. Repeatedly attempt to validate and store the invoice until successful:
            - Validate the invoice using the database (`check_invoice`).
            - Add the invoice to the database (`add_invoice`).
            - Build the invoice PDF (`build_pdf`).
        3. If validation fails due to known errors, retry with a newly generated invoice.

    Exceptions handled:
        TVAError: Raised when there is an issue with tax calculation or validation.
        InvalidInvoice: Raised when the invoice data structure is malformed.

    Returns:
        None
    """
    db = InvoiceDataBase()
    logger.info(f"DataBase {db}")

    while True:
        invoice = generate_invoice()

        try:
            db.check_invoice(invoice)
            db.add_invoice(invoice)
            invoice.build_pdf()
            logger.info("Success")
            exit()

        except (TVAError, InvalidInvoice) as err:
            logger.error(f"Must redefine invoice")


def manual_setup():
    """
    Manually initialize the application's required resources and update the global DataDir configuration.

    This function performs the following steps:
      1. Initializes the paths for `data.json` and `database.json` by calling
         `init_data_and_db()`.
      2. Initializes the invoice directory via `init_invoice()`.
      3. Updates the `DataDir` object with the resolved paths for:
         - data file
         - database file
         - invoice directory

    This ensures that all core data locations are properly registered before the application runs.

    Returns:
        None
    """
    data, database = init_data_and_db()
    invoice_dir = init_invoice()
    DataDir.update_data_path(data)
    DataDir.update_database_path(database)
    DataDir.update_invoice_dir(invoice_dir)

def generate_invoice():
    """
    Interactively create an invoice by prompting the user for details.

    The function will ask the user to:
      - Select a work period date (month and year are extracted).
      - Enter the number of work days.
      - Specify whether TVA (VAT) is applicable.
      - Confirm before finalizing.

    Returns:
        Invoice: A new invoice object with the provided details.
    """

    while True:

        logger.info("Enter details for invoice generation")

        # set up date
        period_date = get_period()
        period_month = format_date(period_date, "MMMM", locale="fr").capitalize()
        period_year = period_date.year

        logger.info(f"Work period set to {period_month}-{period_year}")

        # set up n days
        while True:
            n_days = input("Quantity days (j) : ")
            try:
                n_days = float(n_days)
                break
            except (ValueError, TypeError):
                pass

        # set up TVA
        TVA = input("TVA applicable (y/n) : ")
        TVA = True if TVA.lower() == "y" else False

        invoice = Invoice(
            period_month=period_month, period_year=period_year, quantity=n_days, unit_price=485, TVA=TVA
        )

        # check before continuing
        ans = input("Continue (y/n): ")
        if ans.lower() == "y":
            return invoice

def find_files_based_on_key(_dir):
    """
    Search for JSON files in a given directory whose filenames contain
    the keywords 'data' or 'database', and return the first match for each.

    Args:
        _dir (str): Path to the directory to search.

    Returns:
        dict: Dictionary with the following keys:
            'data' (str or None): Absolute path to the first JSON file
                containing 'data' in its name, or None if not found.
            'database' (str or None): Absolute path to the first JSON file
                containing 'database' in its name, or None if not found.

    Notes:
        The search is non-recursive; only files directly inside `_dir`
        are considered. Matching is not case-sensitive.
    """
    fpath = {'data': None, 'database':None}

    for key in fpath:
        for filename in os.listdir(_dir):
            if filename.endswith('.json') and key in filename.lower():
                fpath[key] = os.path.join(_dir, filename)
                break
    return fpath


def init_data_and_db():
    """
    Initialize input data and database file paths.

    The function prompts the user to provide the path to a data folder. It validates the input to ensure it is a valid
    directory. If not, an error is logged and the user is asked again.

    Once a valid folder is provided, the function searches for required files (data and database) using
    `find_files_based_on_key`. If both files are found, their paths are logged and returned. If one or both files are
    missing, an error is logged and the user is prompted again.

    Returns:
        tuple[str, str]: A tuple containing the paths to the data file and
        the database file, respectively.
    """

    while True:

        ans = input("Input data folder: ")

        if not os.path.isdir(ans):
            logger.error(f"{ans!r} is not a valid path")
        else:
            fpath = find_files_based_on_key(ans)
            data = fpath.get('data', None)
            database = fpath.get('database', None)
            msg = (f"found :\n"
                   f" - data     : {data!r} \n"
                   f" - database : {database!r}")
            logger.info(msg)

            if data is None or database is None:
                logger.error("missing data file")
            else:
                return data, database


def init_invoice():
    """
    Prompt the user for the invoice folder path.

    The function repeatedly asks the user to input a path to the invoice folder. It checks whether the provided path
    exists and is a directory. If the input is invalid, an error is logged and the user is prompted again.

    Once a valid directory is entered, the function returns its path.

    Returns:
        str: The absolute or relative path to the invoice folder provided by the user.
    """

    while True:
        ans = input("Invoice folder: ")
        if not os.path.isdir(ans):
            logger.error(f"{ans!r} is not a valid path")
        else:
            return ans


def get_period():
    """
    Prompt the user for a reporting period date.

    By default, the period is set to 15 days before today's date. The user is prompted whether they want to use this
    default value. If not, the function allows the user to define a custom period by manually entering a month and year.

    The function validates the custom input and only accepts valid dates (with day fixed to 1). Invalid inputs will
    prompt the user again until a valid date is provided.

    Returns:
        datetime.date: A date object representing the first day of the selected period.
                       Either 15 days before today or the user-provided month/year.
    """

    def custom_period():
        """
        Prompt the user to define a custom reporting period.

        The user is asked to input a month and a year. Inputs are validated by attempting to create a `datetime.date`
        object (with day fixed to 1). If the input cannot be converted into a valid date, an error is logged and the
        user is prompted again until valid values are entered.

        Returns:
            datetime.date: A valid date object representing the first day of the
                           custom month and year provided by the user.
        """
        while True:
            period_month = input(f"period month : ")
            period_year = input(f"period year : ")
            try:
                # try date
                period_date = date(year=int(period_year), month=int(period_month), day=1)
                return period_date
            except (TypeError, ValueError) as err:
                logger.error(f"Incorrect period {err}")

    period_date = date.today() - timedelta(days=15)
    ans = input(f"Use work period {period_date.strftime("%m-%Y")} (y/n)? ")

    if ans.lower() != 'y':
        period_date = custom_period()

    return period_date

