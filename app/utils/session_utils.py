import uuid
import datetime
from app import db
from app.models.erp_models import Session

def create_session(user_id, expiration_minutes):
    """Create a new session for the given user."""
    session_key = str(uuid.uuid4())  # Generate a unique session key
    now = datetime.datetime.utcnow()
    expires_at = now + datetime.timedelta(minutes=expiration_minutes)

    # Ensure no duplicate session for the user
    existing_session = Session.query.filter_by(user_id=user_id).first()
    if existing_session:
        db.session.delete(existing_session)  # Remove the old session

    print(expires_at)
    # Create a new session
    new_session = Session(user_id=user_id, session_key=session_key, created_at=now, expires_at=expires_at)
    db.session.add(new_session)
    db.session.commit()

    return session_key

def validate_session(session_key):
    """Validate if the session key is active."""
    session = Session.query.filter_by(session_key=session_key).first()
    if not session or not session.is_active():
        return False  # Session expired or invalid

    # # Extend session expiration on activity (optional)
    # session.expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    # db.session.commit()
    return True

def delete_session(session_key):
    """Delete a session upon logout."""
    session = Session.query.filter_by(session_key=session_key).first()
    if session:
        db.session.delete(session)
        db.session.commit()
