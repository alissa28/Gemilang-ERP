from flask import Blueprint, render_template, request, jsonify
from app.models.operational_models import Inventory, PurchaseDetail, SaleDetail
from app import db
from app.utils.auth_utils import privilege_required

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
@privilege_required('view_reports')
def index():
    return render_template('inventory.html')

# Inventory CRUD operations
@inventory_bp.route('/insert', methods=['POST'])
def create_inventory():
    data = request.json
    inventory = Inventory(
        name=data['name'],
        description=data.get('description'),
        category_id=data.get('category_id'),
        current_stock=data.get('current_stock', 0),
        reorder_level=data.get('reorder_level'),
        unit_price=data['unit_price'],
        unit=data['unit']
    )
    db.session.add(inventory)
    db.session.commit()
    return jsonify(inventory), 201

# New function to add a new inventory item
@inventory_bp.route('/add', methods=['POST'])
def add_inventory_item():
    data = request.json
    new_item = Inventory(
        name=data['name'],
        description=data.get('description'),
        category_id=data.get('category_id'),
        current_stock=data.get('current_stock', 0),
        reorder_level=data.get('reorder_level'),
        unit_price=data['unit_price'],
        unit=data['unit']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@inventory_bp.route('/<int:item_id>', methods=['GET'])
def get_inventory(item_id):
    inventory = Inventory.query.get_or_404(item_id)
    return jsonify(inventory)

@inventory_bp.route('/<int:item_id>', methods=['PUT'])
def update_inventory(item_id):
    data = request.json
    inventory = Inventory.query.get_or_404(item_id)
    inventory.description = data.get('description', inventory.description)
    inventory.unit_price = data.get('unit_price', inventory.unit_price)
    inventory.unit = data.get('unit', inventory.unit)
    db.session.commit()
    return jsonify(inventory.to_dict())

@inventory_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_inventory(item_id):
    inventory = Inventory.query.get_or_404(item_id)
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({'message': 'Inventory item deleted'})

@inventory_bp.route('/all', methods=['GET'])
def get_all_inventory():
    inventory_items = Inventory.query.all()
    return jsonify([item.to_dict() for item in inventory_items])

@inventory_bp.route('/count', methods=['GET'])
def get_inventory_count():
    count = Inventory.query.count()
    return jsonify({'count': count})

@inventory_bp.route('/transactions', methods=['GET'])
def get_inventory_transactions():
    transactions = []

    purchase_details = PurchaseDetail.query.all()
    for detail in purchase_details:
        transactions.append({
            'item_id': detail.item_id,
            'item_name': detail.item.name,
            'unit_price': detail.unit_price,
            'current_stock': detail.item.current_stock,
            'type': 'purchase',
            'quantity': detail.quantity,
            'date': detail.purchase.purchase_date
        })

    sale_details = SaleDetail.query.all()
    for detail in sale_details:
        transactions.append({
            'item_id': detail.item_id,
            'item_name': detail.item.name,
            'unit_price': detail.unit_price,
            'current_stock': detail.item.current_stock,
            'type': 'sale',
            'quantity': detail.quantity,
            'date': detail.sale.sale_date
        })

    return jsonify(transactions)