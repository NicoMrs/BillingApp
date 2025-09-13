# paths
import os
from os.path import dirname as up
from functools import wraps
from .setup_logger import logger

def check_existing_path(func):
    @wraps(func)
    def inner(cls, file_path):
        if not os.path.isfile(file_path):
            logger.warning(f"Data path {file_path!r} does not exist. Could not update.")
            return # avoid unnecessary updates
        return func(cls, file_path)
    return inner

def check_existing_dir(func):
    @wraps(func)
    def inner(cls, _dir):
        if not os.path.isdir(_dir):
            logger.warning(f"Directory {_dir!r} does not exist. It is created.")
            os.mkdir(_dir)
        return func(cls, _dir)
    return inner


class DataDir:

    INVOICE_DIR = "./invoices"
    DATA = "./data/data.json"
    DATABASE = "./data/database.json"

    DUMMY_DATA = os.path.join(up(up(__file__)), 'data', 'dummy_data.json')
    DUMMY_DATABASE = os.path.join(up(up(__file__)), 'data', 'dummy_database.json')

    @classmethod
    @check_existing_path
    def update_data_path(cls, data_path):
        cls.DATA = data_path

    @classmethod
    @check_existing_path
    def update_database_path(cls, database_path):
        cls.DATABASE = database_path

    @classmethod
    @check_existing_dir
    def update_invoice_dir(cls, invoice_dir):
        cls.INVOICE_DIR = invoice_dir