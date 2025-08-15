# invoice.py

import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from .utils import *
from .template import BuildPDFMixin, footer
from ..utils.paths import DataDir
from ..utils.setup_logger import logger
from datetime import datetime


__all__ = ["Invoice"]

class Invoice(BuildPDFMixin):

    def __init__(self, period_month, period_year, quantity, unit_price=485, TVA=False):

        self.period_month = period_month
        self.period_year = period_year
        self.TVA = TVA
        self.unit_price = unit_price
        self.quantity = quantity
        self.is_valid = None

        if not os.path.isfile(DataDir.DATA):
            logger.warning(f"Custom data {DataDir.DATA!r} not found. Defaulted to dummy data.")
            logger.info(f"Change data dir with <DataDir.update_data_path(data_path)> before running script.")
            self.setup_file = DataDir.DUMMY_DATA
        else:
            self.setup_file = DataDir.DATA

        self.total_HT = self.quantity * self.unit_price
        now = datetime.now()
        self.invoice_date = now.strftime("%d/%m/%Y")
        self.number = int(f"{now.year}{now.month:02}01")

        self._elements = []
        self._setup_data()

        logger.info(f"invoice {self} generated")

    def _setup_data(self):
        """Load company, client, and bank data from JSON setup file."""
        try:
            with open(self.setup_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.company = Company(**data["company"])
            self.client = Company(**data["client"])
            self.bank = Bank(**data["bank_account"])

        except FileNotFoundError:
            raise FileNotFoundError(f"Setup file '{self.setup_file}' not found.")
        except KeyError as e:
            raise KeyError(f"Missing required key in setup file: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in '{self.setup_file}': {e}")


    def to_dict(self):
        """ transform args into dict """
        args = (
            "number",
            "period_month",
            "period_year",
            "quantity",
            "unit_price",
            "total_HT",
            "TVA",
            "invoice_date"
        )
        return {arg:getattr(self, arg) for arg in args}

    def __repr__(self):
        cls_name = type(self).__name__
        return (
            f"{cls_name}("
            f"number={self.number}, "
            f"period_month={self.period_month!r}, "
            f"period_year={self.period_year!r}, "
            f"quantity={self.quantity}, "
            f"unit_price={self.unit_price}, "
            f"apply_TVA={self.TVA})"
        )

    def __str__(self):
        return (f"<Invoice: n°{self.number} - {self.period_month} {self.period_year} - "
                f"days={self.quantity} - revenue_HT={self.total_HT} TVA={self.TVA}>")

    def build_pdf(self):
        pdf_invoice = f"facture_{self.number}_{self.company.name[:3]}.pdf"
        doc = SimpleDocTemplate(filename=os.path.join(DataDir.INVOICE_DIR, pdf_invoice), pagesize=A4)

        self._header()
        self._company_details()
        self._client_details()
        self._period()
        self._invoice_details()
        self._invoice_data()
        self._billing()

        if not self.is_valid:
            logger.warning(f"{self} has not been checked!")

        doc.build(self._elements ,onFirstPage=footer(self.company, self.TVA))
        logger.info(f"✅  PDF billing generated : {pdf_invoice}")