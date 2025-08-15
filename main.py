from billing.invoice import Invoice
from billing.database import InvoiceDataBase
from billing.utils.paths import DataDir
from billing.utils.setup_logger import logger

# ** Set up data directories
DataDir.update_invoice_dir("invoices")
DataDir.update_data_path("./data/data.json")
DataDir.update_database_path("./data/db_2025.json")

# ** Generate Invoice
invoice_1 = Invoice(period_month="Août", period_year = "2025", quantity=20.5, unit_price=485, TVA = False)
invoice_2 = Invoice(period_month="Août", period_year = "2025", quantity=17, unit_price=485, TVA = False)

# ** Billing Directories
db = InvoiceDataBase()
logger.info(f"DataBase {db}")

# ** Add Invoice to database
db.add_invoice(invoice_1)
db.add_invoice(invoice_2)

# ** Add Invoice to database
invoice_1.build_pdf()
invoice_2.build_pdf()


