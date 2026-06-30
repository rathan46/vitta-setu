from flask import Blueprint, request, jsonify, url_for
from app.middleware.auth_middleware import require_api_key
from app.services import payment_service
from app.middleware.rate_limit import rate_limit

api_v1_bp = Blueprint('api_v1', __name__)

@api_v1_bp.route('/create-payment', methods=['POST'])
@rate_limit(limit=100, per=60)
@require_api_key
def create_payment():
    data = request.get_json()
    
    required_fields = ['amount', 'upi_address', 'target_callback_url', 'return_url']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
            
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than 0'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid amount format'}), 400
        
    merchant = request.merchant
    
    session = payment_service.create_payment_session(
        merchant_id=merchant.id,
        amount=amount,
        upi_address=data['upi_address'],
        callback_url=data['target_callback_url'],
        return_url=data['return_url'],
        raw_request=data,
        kwargs={
            'merchant_transaction_id': data.get('merchant_transaction_id'),
            'currency': data.get('currency', 'INR'),
            'customer_name': data.get('customer_name'),
            'customer_email': data.get('customer_email'),
            'customer_phone': data.get('customer_phone')
        }
    )
    
    # URL for the payment page
    from run import app
    domain = app.config.get('APP_DOMAIN', 'http://localhost:5000')
    payment_url = f"{domain}/payment/{session.temporary_token}"
    
    return jsonify({
        'status': 'success',
        'session_id': session.id,
        'temporary_token': session.temporary_token,
        'payment_url': payment_url,
        'expiry_time': session.expiry_time.isoformat()
    }), 201
