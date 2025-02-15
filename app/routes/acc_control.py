from flask import Blueprint, request, jsonify
from app.utils.db_utils import (
    create_role, get_role, update_role, delete_role,
    create_user, get_user, update_user, delete_user,
    get_all_users, get_all_roles, get_all_privileges, modify_role_privileges
)
from app.utils.session_validation import session_required

acc_control = Blueprint('acc_control', __name__)

# Role routes
@acc_control.route('/roles', methods=['POST'])
@session_required
def create_role_route():
    data = request.json
    role = create_role(data['name'], data.get('description'))
    return jsonify(role.to_dict()), 201

@acc_control.route('/roles/<int:role_id>', methods=['GET'])
@session_required
def get_role_route(role_id):
    role = get_role(role_id)
    return jsonify(role.to_dict())

@acc_control.route('/roles/<int:role_id>', methods=['PUT'])
@session_required
def update_role_route(role_id):
    data = request.json
    role = update_role(role_id, data.get('name'), data.get('description'))
    modify_role_privileges(role_id, data.get('privilege_ids', []))
    return jsonify(role.to_dict())

@acc_control.route('/roles/<int:role_id>', methods=['DELETE'])
@session_required
def delete_role_route(role_id):
    role = delete_role(role_id)
    return jsonify(role.to_dict())

# User routes
@acc_control.route('/users', methods=['POST'])
@session_required
def create_user_route():
    data = request.json
    user = create_user(data['username'], data['email'], data['password'], data['role_id'])
    return jsonify(user.to_dict()), 201

@acc_control.route('/users/<int:user_id>', methods=['GET'])
@session_required
def get_user_route(user_id):
    user = get_user(user_id)
    return jsonify(user.to_dict())

@acc_control.route('/users/<int:user_id>', methods=['PUT'])
@session_required
def update_user_route(user_id):
    data = request.json
    user = update_user(user_id, data.get('username'), data.get('email'), data.get('password'), data.get('role_id'))
    return jsonify(user.to_dict())

@acc_control.route('/users/<int:user_id>', methods=['DELETE'])
@session_required
def delete_user_route(user_id):
    user = delete_user(user_id)
    return jsonify(user.to_dict())

# Fetch all users
@acc_control.route('/users', methods=['GET'])
@session_required
def get_all_users_route():
    users = get_all_users()
    return jsonify([user.to_dict() for user in users])

# Fetch all roles
@acc_control.route('/roles', methods=['GET'])
@session_required
def get_all_roles_route():
    roles = get_all_roles()
    return jsonify([role.to_dict() for role in roles])

# Fetch all privileges
@acc_control.route('/privileges', methods=['GET'])
@session_required
def get_all_privileges_route():
    privileges = get_all_privileges()
    return jsonify([privilege.to_dict() for privilege in privileges])