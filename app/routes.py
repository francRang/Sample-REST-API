from logging import error
from flask import request, abort, jsonify
from flask import current_app as app
from .models import db, Customer
from .helpers import respond, check_query_param_contains_quotes, convert_ascii_with_quotes_to_string_with_no_quotes
from sqlalchemy.exc import DataError

db.create_all()
db.session.commit()

@app.errorhandler(404)
def resource_not_found(e):
    """Generic error handler for errors not specified"""
    return jsonify(error=str(e)), 404

@app.route("/customers", methods=['GET'])
def get_all_customers():
    """A function to retrieve all customers from the database based on a query parameter of city.
    Defaults to all if no parameter.
    ---
    get:
      description: Get all customers that match criteria,
      responses:
        200: Successfull, returns customer(s).
        404: Not found, no costumers in the database.
    """
    if "city" not in request.args:
        customers: list = Customer.query.all()
        if customers is None:
            abort(404, description="There are no customers to retrieve.")
        return respond(customers, 200)
    else:
        city: str = request.args.get("city")
        ascii_list: list = []

        if not check_query_param_contains_quotes(city, ascii_list):
            abort(404, description=f"There are no customers living in {city}.")

        city = convert_ascii_with_quotes_to_string_with_no_quotes(ascii_list)
        all_customers_in_given_city: list = Customer.query.filter_by(city=city).all()

        if all_customers_in_given_city is None or len(all_customers_in_given_city) == 0:
            abort(404, description=f"There are no customers living in {city}.")
        return respond(all_customers_in_given_city, 200)

@app.route("/customers/<int:customerId>", methods=['GET'])
def get_customer_for_given_customerid(customerId: int):
    """A function to retrieve a customer from the database based on a path parameter of customerId.
    ---
    get:
      description: Get all the one customer that matches criteria,
      responses:
        200: Successfull, returns customer(s).
        404: Not found, no costumers in the database.
    """
    customer:str = Customer.query.filter_by(customer_id=customerId).first()

    if customer is None:
        abort(404, description=f"Customer with id of {customerId} does not exist.")
    
    return respond(customer, 200)

@app.route("/customers", methods=['POST'])
def add_a_customer():
    """A function to a a customer to the database based on a JSON request body with the following customer data:
    - First Name
    - Last Name
    - Email Address
    - Address
    - City
    - State
    - Zip
    ---
    post:
      description: Post a costumer to the database, return added costumer with newly assigned id if successful.
      responses:
        200: Successfull, returns customer(s).
        422: Invalid Input, missing parameters and/or incorrect type/type violation.
        409: Duplicate value, email already in the database.
    """
    customer_data = request.json
    if Customer.query.filter_by(email=customer_data["email"]).first() is None:
        try:
            new_customer_to_add = Customer(first_name=customer_data["first_name"], last_name=customer_data["last_name"],
            email=customer_data["email"], address=customer_data["address"], city=customer_data["city"],
            state=customer_data["state"], zip_code=customer_data["zip"])

            db.session.add(new_customer_to_add)
            db.session.commit()

            return respond(new_customer_to_add, 200)
        except (KeyError, DataError):
            return jsonify({"error":(f'{422} Invalid Input: Make sure all necessary parameters are passed and make sure data type is correct.')}), 409, {'Content-Type': 'application/json'}
    else:
        return jsonify({"error":(f'{409} Duplicate Value: Email {customer_data["email"]} is taken.')}), 409, {'Content-Type': 'application/json'}
