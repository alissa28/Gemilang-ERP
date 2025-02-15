from app import create_app, db
from app.models.operational_models import Customer

app = create_app()

with app.app_context():
    # Create a default customer
    default_customer = Customer(
        name='Default',
        phone='1234567890',
        email='default@example.com',
        address='123 Default St, Default City, Default Country'
    )
    db.session.add(default_customer)
    db.session.commit()

    print("Default customer added successfully.")