from flask import Blueprint, render_template, request, jsonify, redirect
from app.services import payment_service
from app.utils.qr_generator import generate_qr_base64
import urllib.parse
from datetime import datetime

payment_bp = Blueprint('payment', __name__)

def is_mobile(user_agent):
    if not user_agent:
        return False
    mobile_keywords = ['Mobile', 'Android', 'iPhone', 'iPad', 'Windows Phone']
    return any(keyword in user_agent for keyword in mobile_keywords)

@payment_bp.route('/<token>', methods=['GET'])
def view_payment_page(token):
    session = payment_service.get_session(token)
    if not session:
        return render_template('payment/error.html', message="Invalid payment session"), 404
        
    if session.state == 'EXPIRED':
        return render_template('payment/expired.html', session=session)

    if session.state in ['SUCCESS', 'FAILED', 'CANCELLED', 'UNKNOWN']:
        # If it's already finished, redirect to return URL immediately or show state
        return render_template('payment/finished.html', session=session)
        
    user_agent = request.headers.get('User-Agent', '')
    client_is_mobile = is_mobile(user_agent)
    
    # Update device info if first time opening
    tx = session.transactions[0] if session.transactions else None
    if tx and not tx.customer_device:
        device_info = {
            'customer_device': 'Mobile' if client_is_mobile else 'Desktop',
            'user_agent': user_agent,
            'ip_address': request.remote_addr
        }
        payment_service.update_state(session.id, 'WAITING', device_info=device_info)

    qr_data = None
    upi_intent_url = None
    
    base_upi_url = f"upi://pay?pa={session.upi_address}&pn={urllib.parse.quote(session.merchant.business_name)}&am={session.amount}&cu={session.currency}&tr={session.id}"

    if client_is_mobile:
        upi_intent_url = base_upi_url
    else:
        # Generate QR code containing the payment URL so scanning it opens this same page on mobile
        from run import app
        domain = app.config.get('APP_DOMAIN', 'http://localhost:5000')
        payment_url = f"{domain}/payment/{session.temporary_token}"
        qr_data = generate_qr_base64(payment_url)
        if tx and not tx.qr_generated:
            tx.qr_generated = True
            from app.extensions import db
            db.session.commit()

    return render_template('payment/pay.html', 
                           session=session, 
                           merchant=session.merchant,
                           is_mobile=client_is_mobile,
                           qr_data=qr_data,
                           upi_intent_url=upi_intent_url)

@payment_bp.route('/<token>/response', methods=['POST'])
def receive_response(token):
    session = payment_service.get_session(token)
    if not session:
        return jsonify({'error': 'Invalid session'}), 404
        
    data = request.get_json()
    status = data.get('status', 'UNKNOWN') # SUCCESS, FAILED, CANCELLED, UNKNOWN
    
    # The frontend submits this when the UPI app returns control.
    # We treat it as a signal, update state, and trigger callback.
    payment_service.update_state(session.id, status)
    
    # Return the return_url for frontend to redirect
    tx = session.transactions[0]
    return jsonify({
        'status': 'processed',
        'return_url': tx.return_url
    })
