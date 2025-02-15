from app import create_app, db
from app.models.erp_models import Role, Privilege, User

app = create_app()

with app.app_context():
    # Create roles
    admin_role = Role(name='Admin', description='Administrator with full access')
    user_role = Role(name='User', description='Regular user with limited access')
    db.session.add_all([admin_role, user_role])

    # Create privileges
    manage_users = Privilege(name='manage_users', description='Can manage users')
    view_reports = Privilege(name='view_reports', description='Can view reports')
    operational = Privilege(name='operational', description='Basic Functions')
    db.session.add_all([manage_users, view_reports, operational])

    # Assign privileges to roles
    admin_role.privileges.extend([manage_users, view_reports, operational])
    user_role.privileges.append(operational)
    db.session.commit()

    # Create an admin user
    admin_user = User(username='admin', email='admin@example.com', role=admin_role)
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    db.session.commit()

    # Create a regular user
    user = User(username='user', email="",role=user_role)
    user.set_password('user123')
    db.session.add(user)
    db.session.commit()

    print("Initial data seeded!")
