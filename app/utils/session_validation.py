from flask import session, redirect, url_for, flash, make_response
from app.utils.session_utils import validate_session

def session_required(view):
    """Decorator to ensure a valid session."""
    from functools import wraps

    @wraps(view)
    def wrapped_view(**kwargs):
        session_key = session.get('session_key')
        print(session.items())
        print(session.get('session_key'))
        if not session_key or not validate_session(session_key):
            flash('Your session has expired. Please log in again.', 'warning')
            print("session expired")
            response = make_response(redirect(url_for('auth.login')))
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response
        response = make_response(view(**kwargs))
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    return wrapped_view
