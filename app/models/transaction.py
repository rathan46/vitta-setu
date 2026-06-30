from datetime import datetime
from app.extensions import db

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.String(36), primary_key=True) # Transaction ID
    merchant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payment_session_id = db.Column(db.String(36), db.ForeignKey('payment_sessions.id'), nullable=False)
    merchant_transaction_id = db.Column(db.String(100), nullable=True)
    temporary_token = db.Column(db.String(100), nullable=False)
    
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), default='INR')
    upi_address = db.Column(db.String(100), nullable=False)
    
    customer_name = db.Column(db.String(100), nullable=True)
    customer_email = db.Column(db.String(120), nullable=True)
    customer_phone = db.Column(db.String(20), nullable=True)
    customer_device = db.Column(db.String(255), nullable=True) # Mobile/Desktop
    os = db.Column(db.String(100), nullable=True)
    browser = db.Column(db.String(100), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    
    payment_status = db.Column(db.String(20), default='PENDING') # SUCCESS, FAILED, CANCELLED, UNKNOWN, PENDING
    utr_number = db.Column(db.String(100), nullable=True)
    failure_reason = db.Column(db.Text, nullable=True)
    manual_verification_status = db.Column(db.String(20), nullable=True) # COMPLETED, PENDING, REJECTED
    
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    payment_time = db.Column(db.DateTime, nullable=True)
    completion_time = db.Column(db.DateTime, nullable=True)
    
    qr_generated = db.Column(db.Boolean, default=False)
    
    callback_url = db.Column(db.String(255), nullable=False)
    return_url = db.Column(db.String(255), nullable=False)
    
    raw_request = db.Column(db.JSON, nullable=True)
    raw_response = db.Column(db.JSON, nullable=True)

    merchant = db.relationship('User', backref=db.backref('transactions', lazy=True))
    session = db.relationship('PaymentSession', backref=db.backref('transactions', lazy=True))
