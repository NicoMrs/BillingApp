# Billing System

I have programmed this application to help manage my billing as a consultant. 

---
## 1. How does it work ?

This application does:
- automatically generates pdf invoices for your client
- register them in a database to keep your accounting book

You can see example of generated invoices in `invoices` folder. The generate manage 2 types of invoice with and
without TVA.


### a. customize for your need

You need to provide the application:
- a `your_data.json` file containing data about your business. Use the template in `billing\data\dummy_data.json`
- a `your_database.json` file containing stored invoice. Use the template in `billing\data\dummy_db_2025.json`

###  b. code example

````py
from billing.invoice import Invoice
from billing.database import InvoiceDataBase
from billing.utils.paths import DataDir
from billing.utils.setup_logger import logger

# ** Set up data directories
# Update with your data. By default, looks for files and directory below
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

# ** Check invoice : check number and TVA threshold
db.check_invoice(invoice_1)
db.check_invoice(invoice_2)

# ** Add valid invoice to database
db.add_invoice(invoice_1)
db.add_invoice(invoice_2)

# ** Generate PDF Invoice
invoice_1.build_pdf()
invoice_2.build_pdf()
````

---
## 2. Set Up

### a. requirements
Requirements are listed in `requirements.txt`

### b. installation
The application `billing` is packaged as a python librairy. Create a `python 3` environment 
on your machine using `py -m venv .venv` and activate it.

To install the librairy:
- download the repo and run `py setup.py install`.
- Alternatively you can create a distribution file `py setup.py sdist` this will generate `billing-1.0.0.tar.gz` then
  run `pip install billing-1.0.0.tar.gz`