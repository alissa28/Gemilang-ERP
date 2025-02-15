from flask import Blueprint, render_template, jsonify
from app.utils.auth_utils import privilege_required
from app.utils.db_utils import get_all_users, get_all_roles, get_all_privileges, get_role
from app.utils.session_validation import session_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/manage_users')
@privilege_required('manage_users')
@session_required
def manage_users():
    users = get_all_users()
    return render_template('admin_panel/table_users.html', users=users)

@admin_bp.route('/manage_roles')
@privilege_required('manage_users')
@session_required
def manage_roles():
    roles = get_all_roles()
    all_privileges = get_all_privileges()
    return render_template('admin_panel/table_roles.html', roles=roles, all_privileges=all_privileges)

@admin_bp.route('/manage_privileges')
@privilege_required('manage_users')
@session_required
def manage_privileges():
    privileges = get_all_privileges()
    return render_template('admin_panel/table_privileges.html', privileges=privileges)

@admin_bp.route('/')
@privilege_required('manage_users')
@session_required
def admin_panel():
    return render_template('admin_panel/admin_panel.html')

@admin_bp.route('/roles/<int:role_id>', methods=['GET'])
def get_role_details(role_id):
    role = get_role(role_id)
    return jsonify(role)