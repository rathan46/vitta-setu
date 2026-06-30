from datetime import datetime, timedelta
from app.repositories import payment_session_repo, transaction_repo
from app.utils.security import generate_uuid, generate_temporary_token
from app.services.callback_service import CallbackService

class PaymentService:
    def create_payment_session(self, merchant_id, amount, upi_address, callback_url, return_url, raw_request, kwargs=None):
        kwargs = kwargs or {}
        
        # Idempotency check could be added here if merchant_transaction_id is provided
        merchant_transaction_id = kwargs.get('merchant_transaction_id')
        if merchant_transaction_id:
            existing = transaction_repo.model.query.filter_by(
                merchant_id=merchant_id, 
                merchant_transaction_id=merchant_transaction_id
            ).first()
            if existing:
                return existing.session # Return existing session if found (idempotency)

        session_id = generate_uuid()
        temporary_token = generate_temporary_token()
        expiry_time = datetime.utcnow() + timedelta(minutes=10)

        session = payment_session_repo.create(
            id=session_id,
            merchant_id=merchant_id,
            temporary_token=temporary_token,
            amount=amount,
            upi_address=upi_address,
            expiry_time=expiry_time,
            state='CREATED'
        )

        transaction_id = generate_uuid()
        transaction = transaction_repo.create(
            id=transaction_id,
            merchant_id=merchant_id,
            payment_session_id=session_id,
            merchant_transaction_id=merchant_transaction_id,
            temporary_token=temporary_token,
            amount=amount,
            currency=kwargs.get('currency', 'INR'),
            upi_address=upi_address,
            customer_name=kwargs.get('customer_name'),
            customer_email=kwargs.get('customer_email'),
            customer_phone=kwargs.get('customer_phone'),
            callback_url=callback_url,
            return_url=return_url,
            raw_request=raw_request,
            payment_status='PENDING'
        )

        return session

    def get_session(self, token):
        session = payment_session_repo.get_by_token(token)
        if session and session.expiry_time < datetime.utcnow() and session.state not in ['SUCCESS', 'FAILED', 'UNKNOWN', 'CANCELLED']:
            self.update_state(session.id, 'EXPIRED')
        return session

    def update_state(self, session_id, new_state, device_info=None):
        session = payment_session_repo.get_by_id(session_id)
        if not session:
            return False

        session.state = new_state
        payment_session_repo.update(session)

        # Update transaction
        transactions = session.transactions
        if transactions:
            tx = transactions[0]
            if new_state in ['SUCCESS', 'FAILED', 'CANCELLED', 'UNKNOWN']:
                tx.payment_status = new_state
                tx.completion_time = datetime.utcnow()
                if new_state == 'SUCCESS':
                    tx.payment_time = datetime.utcnow()
                
                # Trigger callback queue
                CallbackService.queue_callback(tx.id)

            if device_info:
                if 'customer_device' in device_info: tx.customer_device = device_info['customer_device']
                if 'os' in device_info: tx.os = device_info['os']
                if 'browser' in device_info: tx.browser = device_info['browser']
                if 'ip_address' in device_info: tx.ip_address = device_info['ip_address']
                if 'user_agent' in device_info: tx.user_agent = device_info['user_agent']

            transaction_repo.update(tx)

        return True
