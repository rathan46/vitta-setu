from datetime import datetime
from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    merchant_name = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    business_name = db.Column(db.String(150), nullable=False)
    business_address = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    account_status = db.Column(db.String(20), default='active') # active, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    # Branding Fields
    logo_url = db.Column(db.String(255), nullable=True)
    favicon_url = db.Column(db.String(255), nullable=True)
    primary_color = db.Column(db.String(7), default='#4f46e5')
    accent_color = db.Column(db.String(7), default='#10b981')
    support_email = db.Column(db.String(120), nullable=True)
    support_phone = db.Column(db.String(20), nullable=True)
    footer_text = db.Column(db.String(255), nullable=True)
    payment_success_message = db.Column(db.String(255), nullable=True)
    payment_failure_message = db.Column(db.String(255), nullable=True)
    payment_page_theme = db.Column(db.String(20), default='dark') # dark, light

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
