# database.py

import json
import os
from .utils import TVAError, InvoiceNumberError, InvalidInvoice
from ..utils.setup_logger import logger
from ..utils.paths import DataDir

__all__ = ["InvoiceDataBase"]


class InvoiceDataBase:

    THRESHOLD_TVA = 41_250

    def __init__(self):

        if not os.path.isfile(DataDir.DATABASE):
            logger.warning(f"Custom data {DataDir.DATABASE!r} not found. Defaulted to dummy data.")
            logger.info(f"Change data dir with <DataDir.update_database_path(database_path)> before running script.")
            self.db_file = DataDir.DUMMY_DATABASE
        else:
            self.db_file = DataDir.DATABASE

        self.db = self.load_data_base()

    def __iter__(self):
        return (invoice_dict for invoice_dict in self.db)

    def __len__(self):
        return len(self.db)

    def __repr__(self):
        cls_name = type(self).__name__
        return f"{cls_name}(db_file={self.db_file!r})"

    def add_invoice(self, invoice):
        """ add invoice to database """
        while True:
            ans = input(f"ADD {invoice} to database ? (y/n) ")

            if ans.lower().strip() == "y":
                if invoice.is_valid is None:
                    logger.error(f"Check invoice before adding to database.")
                    return
                elif invoice.is_valid is False:
                    logger.error(f"Cannot add invalid invoice to database.")
                    return
                self.db.append(invoice.to_dict())
                self._save_db(invoice)
                break

            elif ans.lower().strip() == "n":
                logger.info(f"Invoice n°{invoice.number} NOT ADDED to database")
                break

    def _check_tva_threshold(self, invoice):
        """ check TVA is properly accounted for """

        if self.total_HT < self.THRESHOLD_TVA < self.total_HT+invoice.total_HT:
            raise TVAError(f"TVA threshold <{self.THRESHOLD_TVA} euros> is reached at this billing. "
                           f"Current total revenue HT <{self.total_HT} euros> - "
                           f"billing revenue HT <{invoice.total_HT} euros>.")

        if self.total_HT < self.THRESHOLD_TVA and invoice.TVA:
            raise TVAError(f"Total revenue HT <{self.total_HT} euros> is below TVA threshold "
                           f"<{self.THRESHOLD_TVA} euros>. TVA must not be applied on this billing!")

        if self.total_HT > self.THRESHOLD_TVA and not invoice.TVA:
            raise TVAError(f"Total revenue HT <{self.total_HT} euros> is above TVA threshold "
                           f"<{self.THRESHOLD_TVA} euros>. TVA must be applied on this billing!")


    def _check_invoice_number(self, invoice):
        """ check billing number is different from last billing number in database and update it if necessary """
        if len(self) > 0:

            last_invoice = self.db[-1]
            if last_invoice["number"] == invoice.number:
                logger.warning(f"Last billing in database has same number: {invoice.number}. "
                               f"Current billing number is incremented (+1).")
                invoice.number += 1

            if invoice.number < last_invoice["number"]:
                raise InvoiceNumberError(f"Invalid invoice number {invoice.number}. Invoice numbers must be increasing")

    def check_invoice(self, invoice):
        try:
            self._check_tva_threshold(invoice)
            self._check_invoice_number(invoice)
            invoice.is_valid = True
        except (TVAError, InvoiceNumberError) as err:
            raise InvalidInvoice(err) from err


    @property
    def total_HT(self):
        return sum(invoice["total_HT"] for invoice in self)

    def load_data_base(self):
        # Load JSON from file
        with open(self.db_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def _save_db(self, invoice):

        with open(self.db_file, "w") as f:
            json.dump(self.db, f, ensure_ascii=True, indent=4)
        logger.info(f"Invoice n°{invoice.number} ADDED to database")

