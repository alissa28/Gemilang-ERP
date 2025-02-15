import os
from flask_migrate import upgrade
from app import create_app, db

def run_seed_scripts():
    """Run the seed scripts to populate the database."""
    os.system('python seed_inv.py')
    os.system('python seed_customer.py')
    os.system('python seed.py')

def main():
    """Main function to initialize the Flask app, set up the database, and run seed scripts."""
    app = create_app()

    with app.app_context():
        # Initialize the database and apply migrations
        db.create_all()
        upgrade()

        # Run the seed scripts
        run_seed_scripts()

if __name__ == '__main__':
    main()