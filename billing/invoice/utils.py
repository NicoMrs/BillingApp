from dataclasses import dataclass

@dataclass()
class Company:
    name: str
    phone : str = None
    email : str = None
    street : str = None
    postcode : str = None
    country : str = None
    city : str = None
    siren : str = None
    siret : str = None
    tva_number : str = None

@dataclass()
class Bank:
    iban: str
    bic : str