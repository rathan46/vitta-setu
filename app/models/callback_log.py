from datetime import datetime
from app.extensions import db

class CallbackLog(db.Model):
    __tablename__ = 'callback_logs'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(36), db.ForeignKey('transactions.id'), nullable=False)
    
    queued_time = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_time = db.Column(db.DateTime, nullable=True)
    
    response_code = db.Column(db.Integer, nullable=True)
    response_body = db.Column(db.Text, nullable=True)
    
    retry_count = db.Column(db.Integer, default=0)
    final_status = db.Column(db.String(20), default='PENDING') # SUCCESS, FAILED, PENDING
    
    transaction = db.relationship('Transaction', backref=db.backref('callback_logs', lazy=True))
