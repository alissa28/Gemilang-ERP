from flask import session, redirect, url_for, flash
from functools import wraps

def privilege_required(privilege_name):
    """Decorator to check if the user has the required privilege."""
    def decorator(view):
        @wraps(view)
        def wrapped_view(**kwargs):
            from app.models.erp_models import User
            print(session)
            user_id = session.get('user_id')
            if not user_id:
                flash('You need to log in first.')
                return redirect(url_for('auth.login'))

            # Check if the user has the required privilege
            user = User.query.get(user_id)
            if not user or not user.has_privilege(privilege_name):
                print('Access denied. You do not have the required privilege.')
                return redirect(url_for('main.operational_main'))
            return view(**kwargs)
        return wrapped_view
    return decorator
