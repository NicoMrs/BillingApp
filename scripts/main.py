from billing.invoice import Invoice
from billing.database import InvoiceDataBase
from billing.utils.paths import DataDir
from billing.utils.setup_logger import logger

# ** Set up data directories
# Update with your data. By default, look for file and directories below
# If not found, default to dummy_data.json and dummy_database.json
DataDir.update_invoice_dir("./invoices")
DataDir.update_data_path("./data/data.json")
DataDir.update_database_path("./data/database.json")

# ** Generate Invoice
invoice_1 = Invoice(period_month="Août", period_year = "2025", quantity=20.5, unit_price=485, TVA = True)
invoice_2 = Invoice(period_month="Août", period_year = "2025", quantity=17, unit_price=485, TVA = False)

# ** Load Database
db = InvoiceDataBase()
logger.info(f"DataBase {db}")

# ** Check invoice : number and TVA threshold
db.check_invoice(invoice_1)
db.check_invoice(invoice_2)

# ** Add valid invoice to database
db.add_invoice(invoice_1)
db.add_invoice(invoice_2)

# ** Generate PDF Invoice
invoice_1.build_pdf()
invoice_2.build_pdf()


