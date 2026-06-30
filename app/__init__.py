from flask import Flask
from app.config import config_by_name
from app.extensions import db, migrate, login_manager, scheduler

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    if not scheduler.running:
        scheduler.start()

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.payment_routes import payment_bp
    from app.routes.sse_routes import sse_bp
    from app.routes.api_v1_routes import api_v1_bp
    from app.routes.monitoring_routes import monitoring_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(payment_bp, url_prefix='/payment')
    app.register_blueprint(sse_bp, url_prefix='/payment/stream')
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')
    app.register_blueprint(monitoring_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return db.session.get(User, int(user_id))
