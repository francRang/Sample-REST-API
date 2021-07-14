from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()
DB_URI = os.getenv('DATABASE_URI')

app = Flask(__name__)

#CHANGE THIS TO postgres URI
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app)

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.Integer(10), nullable=False)

@app.route("/customers", methods='GET')
def get_all_customers():
    all_customers = Customer.query.all()
    return all_customers, 200

@app.route("/customers", methods=['GET', 'POST'])
def get_all_customers_from_given_city():
    if request.method == 'POST':
        customer_data = request.json

        new_customer_to_add = Customer(first_name=customer_data["first_name"], last_name=customer_data["last_name"],
        email=customer_data["email"], address=customer_data["address"], city=customer_data["city"],
        state=customer_data["state"], zip_code=customer_data["zip"])

        db.session.add(new_customer_to_add)
        db.session.commit()

        filtered_customer = Customer.query.filter_by(first_name=customer_data["first_name"], last_name=customer_data["last_name"],
        email=customer_data["email"], address=customer_data["address"], city=customer_data["city"],
        state=customer_data["state"], zip_code=customer_data["zip"]).first()

        return filtered_customer, 200
    else:
        city = request.arg.get("city")
        all_customers_in_given_city = Customer.query.filter_by(city=city).all()
        return all_customers_in_given_city, 200

@app.route("/customers/<int:customerId>", methods='GET')
def get_data_for_given_customer(customerId):
    customer = Customer.query.filter_by(customer_id=customerId).first()
    return customer, 200

if __name__ == '__main__':
    app.run(host='localhost',debug=True)