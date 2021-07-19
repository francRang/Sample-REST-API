from . import db
from dataclasses import dataclass

@dataclass
class Customer(db.Model):
    """Db Model for Customers"""
    __tablename__ = 'customers'
    customer_id:id = db.Column(db.Integer, primary_key=True)
    first_name:str = db.Column(db.String(50), nullable=False)
    last_name:str = db.Column(db.String(50), nullable=False)
    email:str = db.Column(db.String(50), unique=True, nullable=False)
    address:str = db.Column(db.String(50), nullable=False)
    city:str = db.Column(db.String(50), nullable=False)
    state:str = db.Column(db.String(50), nullable=False)
    zip_code:int = db.Column(db.Integer, nullable=False)
