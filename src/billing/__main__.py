import argparse

from billing.utils.setup_logger import logger
from .utils.paths import DataDir
from .utils.auto import manual_setup, manage_invoice, find_files_based_on_key


def main():

    parser = argparse.ArgumentParser(
        description="Configure billing system paths (data, database, invoice). "
                    "Falls back to manual setup if incomplete."
    )
    # optional argument with flag
    parser.add_argument("-d", "--data", type=str,
                        help="Path to folder containing data.json and database.json", default=None)
    parser.add_argument("-i", "--invoice", type=str, help="Path to invoice directory", default=None)

    args = parser.parse_args()

    # all arguments must be provided at once, otherwise fall back to manual setup
    if args.data is None or args.invoice is None:
        logger.info("Missing arguments, fall back to manual setup")
        manual_setup()
    else:
        try:
            fpath = find_files_based_on_key(args.data)
            data = fpath.get('data', None)
            database = fpath.get('database', None)

            DataDir.update_data_path(data)
            DataDir.update_database_path(database)
            DataDir.update_invoice_dir(args.invoice)
            logger.info("Successful set up")
        except (TypeError, FileNotFoundError, PermissionError, ValueError) as err:
            logger.error(f"Automatic setup failed: {err}. Falling back to manual setup.")
            manual_setup()

    logger.info(f"Current set up\n{DataDir.status()}")

    manage_invoice()


if __name__ == "__main__":

    main()






