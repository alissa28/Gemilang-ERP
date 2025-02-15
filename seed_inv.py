import pandas as pd
from app import create_app, db
from app.models.operational_models import Inventory, Category

# Create the Flask app
app = create_app()

# Read the spreadsheet file
file_path = 'daftar barang.xlsx'
data = pd.read_excel(file_path)

with app.app_context():
    try:
        # Loop through each row in the spreadsheet
        for _, row in data.iterrows():
            # Retrieve or create the category
            category_name = row.get('Category', 'Uncategorized')  # Default category
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name, description=f"Items under {category_name}")
                db.session.add(category)
                db.session.commit()

            item = Inventory(
                name=row.get('NAMA BARANG', 'Unnamed Item'),           # Default to 'Unnamed Item' if not provided
                description=row.get('SATUAN', ''),                    # Use 'SATUAN' as description, default to empty string
                category_id=category.id,                              # Link to the corresponding category
                current_stock=row.get('CurrentStock', 0),             # Default stock if not present
                reorder_level=row.get('ReorderLevel', 10),            # Default reorder level
                unit_price=row.get('UnitPrice', 10000),                  # Default unit price
                unit=row.get('SATUAN', 'PCS')                            # Default unit
            )

            db.session.add(item)

        # Commit all items to the database
        db.session.commit()
        print("Inventory data seeded successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"Error during seeding: {e}")
