from flask import Blueprint, render_template, request, jsonify
from app.models.operational_models import Sale, SaleDetail, Customer, Inventory
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta
from .fifo_utils import calculate_profit  # Import the FIFO calculation function

sale_bp = Blueprint('sale', __name__)

# Sale CRUD operations
@sale_bp.route('/add', methods=['POST'])
def create_sale():
    data = request.json
    
    # Get customer details
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    total_price = 0
    for item in data['items']:
        total_price += int(item['quantity']) * float(item['unit_price'])

    sale = Sale(
        customer_id=data['customer_id'],
        sale_date=data['date'],
        total_amount=total_price  # Add total price
    )
    db.session.add(sale)
    db.session.flush()  # Get sale.id before committing

    # Add sale details and update inventory
    for item in data['items']:
        sale_detail = SaleDetail(
            sale_id=sale.id,
            item_id=item['item_id'],
            quantity=item['quantity'],
            unit_price=item['unit_price'],
        )
        db.session.add(sale_detail)

        # Update inventory
        inventory_item = Inventory.query.get(item['item_id'])
        if inventory_item:
            inventory_item.current_stock -= int(item['quantity'])
        else:
            return jsonify({'error': f'Inventory item {item["item_id"]} not found'}), 404

    db.session.commit()
    return jsonify({
        'sale_id': sale.id,
        'customer_name': customer.name,
        'customer_address': customer.address,
        'customer_phone': customer.phone,
        'total_amount': total_price
    }), 201

@sale_bp.route('/sales/<int:sale_id>', methods=['GET'])
def get_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    response = sale.to_dict()
    response['details'] = [detail.to_dict() for detail in sale.sale_details]
    response['customer'] = sale.customer.to_dict()
    return jsonify(response)

@sale_bp.route('/sales/<int:sale_id>', methods=['PUT'])
def update_sale(sale_id):
    data = request.json
    sale = Sale.query.get_or_404(sale_id)
    sale.customer_id = data.get('customer_id', sale.customer_id)
    sale.sale_date = data.get('date', sale.sale_date)
    db.session.commit()
    return jsonify(sale.to_dict())

@sale_bp.route('/sales/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    return jsonify({'message': 'Sale deleted'})

@sale_bp.route('/all', methods=['GET'])
def get_all_sales():
    sales = Sale.query.all()
    return jsonify([{
        **sale.to_dict(),
        'details': [detail.to_dict() for detail in sale.sale_details],
        'customer': sale.customer.to_dict()
    } for sale in sales])

from datetime import datetime, timedelta
from sqlalchemy import func

@sale_bp.route('/receipt', methods=['GET'])
def get_receipt():
    sale_id = request.args.get('sale_id')
    if not sale_id:
        # Return empty template with initialized empty data structure
        empty_data = {
            'noFaktur': '',
            'tanggal': '',
            'namaCustomer': '',
            'alamatCustomer': '',
            'noTelpCustomer': '',
            'produk': []
        }
        return render_template('surat/faktur.html', receipt_data=empty_data)
    
    try:
        sale = Sale.query.get(sale_id)
        if not sale:
            raise ValueError('Sale not found')

        receipt_data = {
            'noFaktur': str(sale.id),
            'tanggal': sale.sale_date.strftime('%Y-%m-%d'),
            'namaCustomer': sale.customer.name,
            'alamatCustomer': sale.customer.address,
            'noTelpCustomer': sale.customer.phone,
            'produk': []
        }

        # Ensure sale details are loaded
        for detail in sale.sale_details:
            receipt_data['produk'].append({
                'namaBarang': detail.item.name,
                'hargaSatuan': float(detail.unit_price),
                'kuantitas': detail.quantity,
                'jumlahHarga': float(detail.unit_price * detail.quantity)
            })

        # Debug logging
        print("Receipt data:", receipt_data)
        
        return render_template('surat/faktur.html', receipt_data=receipt_data)
        
    except Exception as e:
        print(f"Error generating receipt: {str(e)}")
        return render_template('surat/faktur.html', receipt_data={'error': str(e), 'produk': []})

@sale_bp.route('/report', methods=['GET'])
def sales_report():
    period = request.args.get('period', 'day')  # Default to 'day' if no period is specified
    today = datetime.now().date()
    start_date = None

    if period == 'day':
        start_date = today
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    elif period == 'month':
        start_date = today.replace(day=1)  # First day of the month
    else:
        return "Invalid period", 400

    # Query sales data based on the selected period
    sales = Sale.query.filter(func.date(Sale.sale_date) >= start_date).all()

    total_sales = sum(sale.total_amount or 0 for sale in sales)
    total_items_sold = sum(sum(detail.quantity for detail in sale.sale_details) for sale in sales)

    # Calculate profit for each sale
    total_profit = 0
    for sale in sales:
        profit = calculate_profit(sale.id)
        sale.profit = profit
        total_profit += profit
        sale.details = sale.sale_details

    return render_template('sale_report.html',
                         sales=sales,
                         total_sales=total_sales,
                         total_items_sold=total_items_sold,
                         total_profit=total_profit,
                         period=period)
