from flask import Blueprint, request, jsonify
from app.models.operational_models import Supplier
from app import db

supplier_bp = Blueprint('supplier', __name__)

# Supplier CRUD operations
@supplier_bp.route('/add', methods=['POST'])
def create_supplier():
    data = request.json
    supplier = Supplier(
        name=data['name'],
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address')
    )
    db.session.add(supplier)
    db.session.commit()
    return jsonify({
        'id': supplier.id,
        'name': supplier.name,
        'phone': supplier.phone,
        'email': supplier.email,
        'address': supplier.address
    }), 201

@supplier_bp.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return jsonify({
        'id': supplier.id,
        'name': supplier.name,
        'phone': supplier.phone,
        'email': supplier.email,
        'address': supplier.address
    })

@supplier_bp.route('/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    data = request.json
    supplier = Supplier.query.get_or_404(supplier_id)
    supplier.name = data.get('name', supplier.name)
    supplier.phone = data.get('phone', supplier.phone)
    supplier.email = data.get('email', supplier.email)
    supplier.address = data.get('address', supplier.address)
    db.session.commit()
    return jsonify({
        'id': supplier.id,
        'name': supplier.name,
        'phone': supplier.phone,
        'email': supplier.email,
        'address': supplier.address
    })

@supplier_bp.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted'})

@supplier_bp.route('/all', methods=['GET'])
def get_all_suppliers():
    suppliers = Supplier.query.all()
    supplier_list = [{
        'id': supplier.id,
        'name': supplier.name,
        'phone': supplier.phone,
        'email': supplier.email,
        'address': supplier.address
    } for supplier in suppliers]
    return jsonify(supplier_list)

@supplier_bp.route('/count', methods=['GET'])
def get_supplier_count():
    count = Supplier.query.count()
    return jsonify({'count': count})