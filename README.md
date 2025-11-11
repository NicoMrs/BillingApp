# Billing System

A Python application to help consultants and freelancers manage billing efficiently.

This tool:
- Automatically generates PDF invoices for clients
- Stores them in a database to maintain an accounting record

Examples of generated invoices can be found in the `invoices/` folder. Two types of invoices are supported: **with** and **without TVA**.

See example below,

![Invoice Example](images/invoice.jpg)


---

## 1. How It Works

To use the application, you need to provide:

- A `your_data.json` file containing your business information  
  → Use the provided template: `billing/data/dummy_data.json`
- A `your_database.json` file containing stored invoices  
  → Use the provided template: `billing/data/dummy_db_2025.json`

### a. option 1 (Preferred)
Run the module directly:

```bash
py -m billing -d input_json_data_folder -i invoices_folder
```
You can also place the `billing.bat` file in your Windows PATH to call the module directly 
from the command line using: `billing`

![Invoice Example](images/cmd.jpg)

###  b. option 2 (import and run programmatically)

Import the librairy and run the `main.py` script

````py
from billing.invoice import Invoice
from billing.database import InvoiceDataBase
from billing.utils.paths import DataDir
from billing.utils.setup_logger import logger

# Set up data directories
DataDir.update_invoice_dir("./invoices")
DataDir.update_data_path("./data/data.json")
DataDir.update_database_path("./data/database.json")

# Generate Invoice
invoice = Invoice(period_month="August", period_year = "2025", quantity=20.5, unit_price=485, TVA = True)

# Load Database
db = InvoiceDataBase()
logger.info(f"DataBase {db}")

# Check invoice : check number and TVA threshold
db.check_invoice(invoice)

# Add valid invoice to database
db.add_invoice(invoice)

# Generate PDF Invoice
invoice.build_pdf()
````

---
## 2. Set Up

### a. requirements
Dependencies are listed in `requirements.txt`

### b. installation
The application `billing` is packaged as a Python library. 

- Create a `Python 3` environment `py -m venv .venv` and activate it `.venv\Scripts\activate`
- Install the library `pip install .`

Alternatively, you can build a source distribution file:
- `py -m build --sdist` this will generate `billing-1.0.0.tar.gz` 
- then `pip install billing-1.0.0.tar.gz`

---
## 3. Output

All generated invoices are saved as PDFs in the invoices directory. Each invoice is also recorded 
in your database file for future reference.

---
## 4. License and Credits

© 2025 Nicolas MAROIS — MIT License
Developed for independent consultants and small businesses.