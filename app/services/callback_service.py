import requests
from datetime import datetime, timedelta
import json
from app.extensions import db, scheduler
from app.models.callback_log import CallbackLog
from app.models.transaction import Transaction
from app.models.api_key import ApiKey
from app.repositories import callback_repo
from app.utils.security import generate_hmac_signature

class CallbackService:
    @staticmethod
    def queue_callback(transaction_id):
        from run import app # Import here to avoid circular imports
        scheduler.add_job(
            id=f"callback_{transaction_id}",
            func=CallbackService._run_in_context,
            args=[transaction_id, 0],
            next_run_time=datetime.utcnow()
        )

    @staticmethod
    def _run_in_context(transaction_id, retry_count):
        from run import app
        with app.app_context():
            CallbackService.execute_callback(transaction_id, retry_count)

    @staticmethod
    def execute_callback(transaction_id, retry_count):
        transaction = Transaction.query.get(transaction_id)
        if not transaction or not transaction.callback_url:
            return

        api_key = ApiKey.query.filter_by(user_id=transaction.merchant_id, is_active=True).first()
        if not api_key:
            return

        timestamp = str(int(datetime.utcnow().timestamp()))
        payload = {
            "transaction_id": transaction.merchant_transaction_id or transaction.id,
            "vitta_setu_id": transaction.id,
            "status": transaction.payment_status,
            "amount": float(transaction.amount),
            "currency": transaction.currency,
            "utr_number": transaction.utr_number,
            "temporary_token": transaction.temporary_token
        }

        signature = generate_hmac_signature(api_key.private_secret, payload, timestamp)

        headers = {
            "Content-Type": "application/json",
            "X-VS-Signature": signature,
            "X-VS-Timestamp": timestamp,
            "X-VS-Transaction": transaction.id
        }

        log = CallbackLog(
            transaction_id=transaction.id,
            retry_count=retry_count
        )
        db.session.add(log)
        
        try:
            response = requests.post(transaction.callback_url, json=payload, headers=headers, timeout=10)
            log.response_code = response.status_code
            log.response_body = response.text[:1000] # store first 1000 chars
            log.delivery_time = datetime.utcnow()
            
            if response.status_code == 200:
                log.final_status = 'SUCCESS'
                transaction.callback_status = 'SUCCESS'
            else:
                log.final_status = 'FAILED'
                CallbackService._schedule_retry(transaction.id, retry_count)
        except Exception as e:
            log.response_body = str(e)
            log.final_status = 'FAILED'
            CallbackService._schedule_retry(transaction.id, retry_count)
            
        db.session.commit()

    @staticmethod
    def _schedule_retry(transaction_id, current_retry):
        from run import app
        max_retries = app.config.get('CALLBACK_MAX_RETRIES', 5)
        if current_retry >= max_retries:
            tx = Transaction.query.get(transaction_id)
            if tx:
                tx.callback_status = 'FAILED'
                db.session.commit()
            return
            
        # Exponential backoff
        delay_seconds = 5 * (2 ** current_retry)
        if delay_seconds > 300: delay_seconds = 300 # Max 5 mins

        scheduler.add_job(
            id=f"callback_{transaction_id}_{current_retry+1}",
            func=CallbackService._run_in_context,
            args=[transaction_id, current_retry + 1],
            next_run_time=datetime.utcnow() + timedelta(seconds=delay_seconds)
        )
