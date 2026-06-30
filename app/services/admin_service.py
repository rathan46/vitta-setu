from app.extensions import db
from app.models.user import User
from app.models.transaction import Transaction
from app.models.payment_session import PaymentSession
from sqlalchemy import func

def get_global_stats():
    """Returns aggregated stats for the entire platform."""
    total_merchants = User.query.filter_by(is_admin=False).count()
    active_merchants = User.query.filter_by(is_admin=False, account_status='active').count()
    
    total_transactions = Transaction.query.count()
    
    successful_txs = Transaction.query.filter_by(payment_status='SUCCESS').count()
    failed_txs = Transaction.query.filter_by(payment_status='FAILED').count()
    unknown_txs = Transaction.query.filter_by(payment_status='UNKNOWN').count()
    
    # Calculate total revenue
    total_revenue_result = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.payment_status == 'SUCCESS')\
        .scalar()
    
    total_revenue = total_revenue_result or 0.0
    
    success_rate = 0
    if total_transactions > 0:
        success_rate = round((successful_txs / total_transactions) * 100, 2)
        
    return {
        'total_merchants': total_merchants,
        'active_merchants': active_merchants,
        'total_transactions': total_transactions,
        'successful_txs': successful_txs,
        'failed_txs': failed_txs,
        'unknown_txs': unknown_txs,
        'total_revenue': round(total_revenue, 2),
        'success_rate': success_rate
    }

def toggle_merchant_status(user_id):
    """Toggles a merchant's account status between active and suspended."""
    user = db.session.get(User, user_id)
    if not user:
        return False, "User not found"
        
    if user.is_admin:
        return False, "Cannot suspend an administrator"
        
    if user.account_status == 'active':
        user.account_status = 'suspended'
    else:
        user.account_status = 'active'
        
    db.session.commit()
    return True, f"Merchant {user.business_name} status updated to {user.account_status}"
