from flask import Blueprint, request, jsonify
from app.models.operational_models import Customer
from app import db

customer_bp = Blueprint('customer', __name__)

# Create a new customer
@customer_bp.route('/add', methods=['POST'])
def create_customer():
    data = request.json
    customer = Customer(
        name=data['name'],
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address')
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201

# Get a specific customer
@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_dict())

# Update a specific customer
@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    customer = Customer.query.get_or_404(customer_id)
    customer.name = data.get('name', customer.name)
    customer.phone = data.get('phone', customer.phone)
    customer.email = data.get('email', customer.email)
    customer.address = data.get('address', customer.address)
    db.session.commit()
    return jsonify(customer.to_dict())

# Delete a specific customer
@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

# Get all customers
@customer_bp.route('/all', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])