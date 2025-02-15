from flask import Blueprint, request, jsonify
from app.models.operational_models import Purchase, PurchaseDetail, Inventory, Supplier
from app import db
from sqlalchemy.exc import SQLAlchemyError

purchase_bp = Blueprint('purchase', __name__)

# Create a new purchase with details and update inventory
@purchase_bp.route('/add', methods=['POST'])
def create_purchase():
    data = request.json
    try:
        purchase = Purchase(
            supplier_id=data['supplier_id'],
            purchase_date=data.get('date')
        )
        db.session.add(purchase)
        db.session.flush()  # Get purchase.id before committing

        # Add purchase details and update inventory
        for item in data['items']:
            purchase_detail = PurchaseDetail(
                purchase_id=purchase.id,
                item_id=item['item_id'],
                quantity=item['quantity'],
                unit_price=item['unit_price']
            )
            db.session.add(purchase_detail)

            # Update inventory
            inventory_item = Inventory.query.get(item['item_id'])
            if inventory_item:
                inventory_item.current_stock += int(item['quantity'])
            else:
                return jsonify({'error': f'Inventory item {item["item_id"]} not found'}), 404

        db.session.commit()
        return jsonify(purchase.to_dict()), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': str(e)}), 500


# Get a specific purchase and its details
@purchase_bp.route('/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    response = purchase.to_dict()
    response['details'] = [{
        **detail.to_dict(),
        'item_name': detail.item.name
    } for detail in purchase.purchase_details]
    response['supplier'] = {
        **purchase.supplier.to_dict(),
        'supplier_name': purchase.supplier.name
    }
    return jsonify(response)


# Update a specific purchase
@purchase_bp.route('/<int:purchase_id>', methods=['PUT'])
def update_purchase(purchase_id):
    data = request.json
    purchase = Purchase.query.get_or_404(purchase_id)
    try:
        purchase.supplier_id = data.get('supplier_id', purchase.supplier_id)
        purchase.purchase_date = data.get('date', purchase.purchase_date)
        db.session.commit()
        return jsonify(purchase.to_dict()), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Delete a purchase and its associated details
@purchase_bp.route('/<int:purchase_id>', methods=['DELETE'])
def delete_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    try:
        db.session.delete(purchase)
        db.session.commit()
        return jsonify({'message': 'Purchase deleted successfully'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Get all purchases with their details
@purchase_bp.route('/all', methods=['GET'])
def get_all_purchases():
    purchases = Purchase.query.all()
    return jsonify([{
        **purchase.to_dict(),
        'details': [{
            **detail.to_dict(),
            'item_name': detail.item.name
        } for detail in purchase.purchase_details],
        'supplier': {
            **purchase.supplier.to_dict(),
            'supplier_name': purchase.supplier.name
        }
    } for purchase in purchases])


@purchase_bp.route('/count', methods=['GET'])
def get_purchase_count():
    count = Purchase.query.count()
    return jsonify({'count': count})