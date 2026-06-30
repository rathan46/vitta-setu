from datetime import datetime
from app.extensions import db

class PaymentSession(db.Model):
    __tablename__ = 'payment_sessions'

    id = db.Column(db.String(36), primary_key=True) # UUIDv4 Session ID
    temporary_token = db.Column(db.String(100), unique=True, nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), default='INR')
    upi_address = db.Column(db.String(100), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_time = db.Column(db.DateTime, nullable=False)
    
    state = db.Column(db.String(20), default='CREATED') 
    # State Machine: CREATED, VALIDATED, WAITING, QR_GENERATED, APP_LAUNCHED, PROCESSING, SUCCESS, FAILED, CANCELLED, UNKNOWN, EXPIRED

    merchant = db.relationship('User', backref=db.backref('payment_sessions', lazy=True))
