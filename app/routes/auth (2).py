from flask import Blueprint, jsonify, request, redirect, url_for, flash, session as flask_session
from flask import render_template
from flask_cors import cross_origin
from app.models.erp_models import User
from app.utils.session_utils import create_session, validate_session, delete_session
from app import db
from app.config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/authenticate', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def authenticate():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Create a new session
            session_key = create_session(user.id, Config.SESSION_EXPIRATION_MINUTES)
            flask_session['session_key'] = session_key
            flask_session['user_id'] = user.id
            flash('Login successful!', 'success')
            print("Login Attempt Successful")

            return redirect(url_for('main.operational_main', _external=True))
        else:
            flash('Invalid username or password', 'danger')
            print("Login Attempt Failed")

            return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
@cross_origin(supports_credentials=True)
def logout():
    session_key = flask_session.get('session_key')
    if session_key:
        delete_session(session_key)
    flask_session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout_button')
@cross_origin(supports_credentials=True)
def logout_button():
    return redirect(url_for('auth.logout'))

@auth_bp.route('/login')
@cross_origin(supports_credentials=True)
def login():
    return render_template('login_page.html')

@auth_bp.route('/get_user_info')
@cross_origin(supports_credentials=True)
def get_user_info():
    user_id = flask_session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            print(user.role.to_dict())
            return jsonify({
                'username': user.username,
                'role': user.role.to_dict()
            })
    return {'error': 'User not found'}, 404 