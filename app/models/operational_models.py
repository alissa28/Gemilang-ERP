import datetime
from app import db, bcrypt

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column('CustomerID', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(255), nullable=False)
    phone = db.Column('Phone', db.String(15))
    email = db.Column('Email', db.String(255), unique=True)
    address = db.Column('Address', db.Text)

    # Relationships
    sales = db.relationship('Sale', back_populates='customer')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column('SupplierID', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(255), nullable=False)
    phone = db.Column('Phone', db.String(15))
    email = db.Column('Email', db.String(255), unique=True)
    address = db.Column('Address', db.Text)

    # Relationships
    purchases = db.relationship('Purchase', back_populates='supplier')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column('CategoryID', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(255), nullable=False)
    description = db.Column('Description', db.Text)

    # Relationships
    inventory_items = db.relationship('Inventory', back_populates='category')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column('ItemID', db.Integer, primary_key=True)
    sku = db.Column('SKU', db.String(64), nullable=False, default='')
    name = db.Column('Name', db.String(255), nullable=False)
    unit = db.Column('Unit', db.String(64), nullable=False)
    description = db.Column('Description', db.Text)
    category_id = db.Column('CategoryID', db.Integer, db.ForeignKey('categories.CategoryID'))
    current_stock = db.Column('CurrentStock', db.Integer, nullable=False, default=0)
    reorder_level = db.Column('ReorderLevel', db.Integer)
    unit_price = db.Column('UnitPrice', db.Numeric(10, 2), nullable=False, default=0.0)

    # Relationships
    category = db.relationship('Category', back_populates='inventory_items')
    purchase_details = db.relationship('PurchaseDetail', back_populates='item')
    sale_details = db.relationship('SaleDetail', back_populates='item')

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'unit': self.unit,
            'description': self.description,
            'category_id': self.category_id,
            'current_stock': self.current_stock,
            'reorder_level': self.reorder_level,
            'unit_price': self.unit_price
        }

class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column('PurchaseID', db.Integer, primary_key=True)
    supplier_id = db.Column('SupplierID', db.Integer, db.ForeignKey('suppliers.SupplierID'))
    purchase_date = db.Column('PurchaseDate', db.DateTime, default=datetime.datetime.utcnow)
    total_amount = db.Column('TotalAmount', db.Numeric(10, 2))

    # Relationships
    supplier = db.relationship('Supplier', back_populates='purchases')
    purchase_details = db.relationship('PurchaseDetail', back_populates='purchase')

    def to_dict(self):
        return {
            'id': self.id,
            'supplier_id': self.supplier_id,
            'purchase_date': self.purchase_date,
            'total_amount': self.total_amount,
            'supplier': self.supplier.to_dict(),
            'details': [detail.to_dict() for detail in self.purchase_details]
        }

class PurchaseDetail(db.Model):
    __tablename__ = 'purchase_details'
    id = db.Column('PurchaseDetailID', db.Integer, primary_key=True)
    purchase_id = db.Column('PurchaseID', db.Integer, db.ForeignKey('purchases.PurchaseID'))
    item_id = db.Column('ItemID', db.Integer, db.ForeignKey('inventory.ItemID'))
    quantity = db.Column('Quantity', db.Integer, nullable=False)
    unit_price = db.Column('UnitPrice', db.Numeric(10, 2), nullable=False)

    # Relationships
    purchase = db.relationship('Purchase', back_populates='purchase_details')
    item = db.relationship('Inventory', back_populates='purchase_details')

    def to_dict(self):
        return {
            'id': self.id,
            'purchase_id': self.purchase_id,
            'item_id': self.item_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'item': self.item.to_dict()
        }

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column('SaleID', db.Integer, primary_key=True)
    customer_id = db.Column('CustomerID', db.Integer, db.ForeignKey('customers.CustomerID'))
    sale_date = db.Column('SaleDate', db.DateTime, default=datetime.datetime.utcnow)
    total_amount = db.Column('TotalAmount', db.Numeric(10, 2))

    # Relationships
    customer = db.relationship('Customer', back_populates='sales')
    sale_details = db.relationship('SaleDetail', back_populates='sale')

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'sale_date': self.sale_date,
            'total_amount': self.total_amount
        }

class SaleDetail(db.Model):
    __tablename__ = 'sale_details'
    id = db.Column('SaleDetailID', db.Integer, primary_key=True)
    sale_id = db.Column('SaleID', db.Integer, db.ForeignKey('sales.SaleID'))
    item_id = db.Column('ItemID', db.Integer, db.ForeignKey('inventory.ItemID'))
    quantity = db.Column('Quantity', db.Integer, nullable=False)
    unit_price = db.Column('UnitPrice', db.Numeric(10, 2), nullable=False)

    # Relationships
    sale = db.relationship('Sale', back_populates='sale_details')
    item = db.relationship('Inventory', back_populates='sale_details')

    def to_dict(self):
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'item_id': self.item_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price
        }

class Forecast(db.Model):
    __tablename__ = 'forecasts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    purchase_forecast = db.Column(db.Float, nullable=False)
    sale_forecast = db.Column(db.Float, nullable=False)