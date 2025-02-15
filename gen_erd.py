import os
from eralchemy import render_er
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import create_app

# Define the output paths for the ERD diagrams
output_dir = 'erd_diagrams'
os.makedirs(output_dir, exist_ok=True)
erp_erd_output = os.path.join(output_dir, 'erp_erd.png')
operational_erd_output = os.path.join(output_dir, 'operational_erd.png')

# Create distinct declarative bases for ERP and Operational models
ERPBase = declarative_base(metadata=MetaData())
OperationalBase = declarative_base(metadata=MetaData())

app = create_app()

with app.app_context():
    # Define engines for ERP and Operational models
    erp_engine = create_engine('sqlite:///erp_temp.db')
    operational_engine = create_engine('sqlite:///operational_temp.db')

    # Ensure ERP models bind and create tables
    ERPBase.metadata.create_all(erp_engine)
    render_er('sqlite:///erp_temp.db', erp_erd_output)
    print(f"ERD for ERP models generated at {erp_erd_output}")
    erp_engine.dispose()

    # Ensure Operational models bind and create tables
    OperationalBase.metadata.create_all(operational_engine)
    render_er('sqlite:///operational_temp.db', operational_erd_output)
    print(f"ERD for Operational models generated at {operational_erd_output}")
    operational_engine.dispose()

# Clean up temporary databases
try:
    os.remove('erp_temp.db')
    os.remove('operational_temp.db')
except FileNotFoundError:
    pass
