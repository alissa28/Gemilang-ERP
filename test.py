from app.utils.session_utils import create_session
from app.config import Config
from app import create_app

app = create_app()

def test_session():
    with app.app_context():
        return create_session(2, 5)

test_session()