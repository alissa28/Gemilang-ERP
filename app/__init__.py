from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
session_manager = Session()
cors = CORS()

def create_app(config_class=Config):
    """
    Application Factory for creating and configuring the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    cors.init_app(app, supports_credentials=True, resources={r"*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    session_manager.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    from app.routes.acc_control import acc_control
    from app.routes.operational.sales import sale_bp
    from app.routes.operational.purchase import purchase_bp
    from app.routes.operational.inventory import inventory_bp
    from app.routes.operational.supplier import supplier_bp
    from app.routes.operational.customer import customer_bp
    from app.routes.operational.forecast import forecast_bp

    from app.routes.operational.forecast import perform_forecast


    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/main')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(acc_control, url_prefix='/acc_control')    
    app.register_blueprint(sale_bp, url_prefix='/sales')
    app.register_blueprint(purchase_bp, url_prefix='/purchases')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(supplier_bp, url_prefix='/suppliers')
    app.register_blueprint(customer_bp, url_prefix='/customers') 
    app.register_blueprint(forecast_bp, url_prefix='/forecast')

    @app.route('/')
    @cross_origin(supports_credentials=True)
    def welcome_page():
        return render_template('welcome.html')

    # Register custom error handlers
    register_error_handlers(app)

    # Initialize and start the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=perform_forecast, trigger="interval", days=1)
    scheduler.start()

    return app

def register_error_handlers(app):
    """
    Register custom error handlers for the application.
    """
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Page not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {"error": "Internal server error"}, 500
