import datetime
from app import db, bcrypt

class RolePrivilege(db.Model):
    """
    Association table for many-to-many relationship between Roles and Privileges.
    """
    __tablename__ = 'role_privileges'
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    privilege_id = db.Column(db.Integer, db.ForeignKey('privileges.id'), primary_key=True)

    def to_dict(self):
        return {
            'role_id': self.role_id,
            'privilege_id': self.privilege_id
        }

class Role(db.Model):
    """
    Represents a user role with a set of privileges.
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)

    privileges = db.relationship(
        'Privilege',
        secondary='role_privileges',
        backref=db.backref('roles', lazy='dynamic')
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'privileges': [privilege.name for privilege in self.privileges]
        }

    def __repr__(self):
        return f"<Role {self.name}>"

class Privilege(db.Model):
    """
    Represents a specific privilege (e.g., 'view_reports', 'manage_users').
    """
    __tablename__ = 'privileges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def __repr__(self):
        return f"<Privilege {self.name}>"

class User(db.Model):
    """
    Represents a user in the system.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        """Hashes and stores the password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks the hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def has_privilege(self, privilege_name):
        """Checks if the user has a specific privilege."""
        return any(privilege.name == privilege_name for privilege in self.role.privileges)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.name 
        }

    def __repr__(self):
        return f"<User {self.username}>"

class Session(db.Model):
    """
    Represents a user session.
    """
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_key = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('sessions', lazy='dynamic'))

    def is_active(self):
        """Check if the session is still valid."""
        return datetime.datetime.utcnow() < self.expires_at

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_key': self.session_key,
            'created_at': self.created_at,
            'expires_at': self.expires_at
        }

    def __repr__(self):
        return f"<Session user_id={self.user_id} expires_at={self.expires_at}>"
