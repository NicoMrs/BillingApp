# setup.py
from setuptools import setup, find_packages

setup(
    name='billing',
    author='Nicolas Marois',
    maintainer='Nicolas Marois',
    version='1.0.0',
    packages=find_packages(),
    scripts=['main.py'],
    package_data={'billing': ['data/dummy_data.json',
                              'data/dummy_db_2025.json']
                  }
)
