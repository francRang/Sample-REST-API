from flask import request, abort, jsonify
from flask import current_app as app
from .models import db, Customer
from .helpers import respond, check_query_param_contains_quotes, convert_ascii_with_quotes_to_string_with_no_quotes
from sqlalchemy.exc import DataError

db.create_all()
db.session.commit()

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.route("/customers", methods=['GET'])
def get_all_customers():
    if "city" not in request.args:
        customers = Customer.query.all()
        if customers is None:
            abort(404, description="There are no customers to retrieve.")
        return respond(customers, 200)
    else:
        city = request.args.get("city")
        ascii_list = []

        if not check_query_param_contains_quotes(city, ascii_list):
            abort(404, description=f"There are no customers living in {city}.")

        city = convert_ascii_with_quotes_to_string_with_no_quotes(ascii_list)
        all_customers_in_given_city = Customer.query.filter_by(city=city).all()

        if all_customers_in_given_city is None or len(all_customers_in_given_city) == 0:
            abort(404, description=f"There are no customers living in {city}.")
        return respond(all_customers_in_given_city, 200)

@app.route("/customers/<int:customerId>", methods=['GET'])
def get_customer_for_given_customerid(customerId):
    customer = Customer.query.filter_by(customer_id=customerId).first()

    if customer is None:
        abort(404, description=f"Customer with id of {customerId} does not exist.")
    
    return respond(customer, 200)

@app.route("/customers", methods=['POST'])
def add_a_customer():
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
