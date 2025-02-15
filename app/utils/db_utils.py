from app.models.erp_models import Role, Privilege, User, Session
from app import db

# Role CRUD operations
def create_role(name, description=None):
    role = Role(name=name, description=description)
    db.session.add(role)
    db.session.commit()
    return role

def get_role(role_id):
    return Role.query.get(role_id)

def update_role(role_id, name=None, description=None):
    role = Role.query.get(role_id)
    if role:
        if name:
            role.name = name
        if description:
            role.description = description
        db.session.commit()
    return role

def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
    return role

# Privilege CRUD operations
def create_privilege(name, description=None):
    privilege = Privilege(name=name, description=description)
    db.session.add(privilege)
    db.session.commit()
    return privilege

def get_privilege(privilege_id):
    return Privilege.query.get(privilege_id)

def update_privilege(privilege_id, name=None, description=None):
    privilege = Privilege.query.get(privilege_id)
    if privilege:
        if name:
            privilege.name = name
        if description:
            privilege.description = description
        db.session.commit()
    return privilege

def delete_privilege(privilege_id):
    privilege = Privilege.query.get(privilege_id)
    if privilege:
        db.session.delete(privilege)
        db.session.commit()
    return privilege

# User CRUD operations
def create_user(username, email, password, role_id):
    user = User(username=username, email=email, role_id=role_id)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user(user_id):
    return User.query.get(user_id)

def update_user(user_id, username=None, email=None, password=None, role_id=None):
    user = User.query.get(user_id)
    if user:
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
        if role_id:
            user.role_id = role_id
        db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user

# Session CRUD operations
def create_session(user_id, session_key, expires_at):
    session = Session(user_id=user_id, session_key=session_key, expires_at=expires_at)
    db.session.add(session)
    db.session.commit()
    return session

def get_session(session_id):
    return Session.query.get(session_id)

def update_session(session_id, session_key=None, expires_at=None):
    session = Session.query.get(session_id)
    if session:
        if session_key:
            session.session_key = session_key
        if expires_at:
            session.expires_at = expires_at
        db.session.commit()
    return session

def delete_session(session_id):
    session = Session.query.get(session_id)
    if session:
        db.session.delete(session)
        db.session.commit()
    return session

# Additional utility functions
def get_roles_by_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user.role
    return None

def user_has_role(user_id, role_name):
    user = User.query.get(user_id)
    if user and user.role.name == role_name:
        return True
    return False

def get_privileges_by_role(role_id):
    role = Role.query.get(role_id)
    if role:
        return role.privileges
    return None

def modify_role_privileges(role_id, privilege_ids):
    role = Role.query.get(role_id)
    if role:
        role.privileges = Privilege.query.filter(Privilege.id.in_(privilege_ids)).all()
        db.session.commit()
    return role

def get_all_users():
    return User.query.all()

def get_all_roles():
    return Role.query.all()

def get_all_privileges():
    return Privilege.query.all()