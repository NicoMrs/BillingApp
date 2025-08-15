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