from app import create_app, db
from app.models.erp_models import Session
import datetime

app = create_app()

with app.app_context():
    now = datetime.datetime.utcnow()
    expired_sessions = Session.query.filter(Session.expires_at < now).all()

    for session in expired_sessions:
        db.session.delete(session)

    db.session.commit()
    print(f"Removed {len(expired_sessions)} expired sessions.")
