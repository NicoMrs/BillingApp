import argparse
from decimal import Decimal
from billing.utils.setup_logger import logger
from billing.database import *

from .utils.auto import init_data_and_db, init_invoice, generate_invoice
from .utils.paths import DataDir
from billing.database.exceptions import TVAError, InvoiceNumberError, InvalidInvoice



if __name__ == "__main__":

    # ** Set up files
    # set up input files
    data, database = init_data_and_db()
    DataDir.update_data_path(data)
    DataDir.update_database_path(database)

    # set up invoice folder
    invoice_dir = init_invoice()
    DataDir.update_invoice_dir(invoice_dir)

    logger.info(f"data set to     : {data!r}")
    logger.info(f"database set to : {database!r}")
    logger.info(f"invoices will be generated at : {invoice_dir!r}")

    db = InvoiceDataBase()
    logger.info(f"DataBase {db}")

    while True:
        # generate invoice
        invoice = generate_invoice()

        try:
            db.check_invoice(invoice)
            db.add_invoice(invoice)
            invoice.build_pdf()
            logger.info("Success")

        except (TVAError, InvoiceNumberError, InvalidInvoice) as err:
            logger.error("Must redfine invoice")
