from flask import Blueprint, Response, stream_with_context
from app.services import payment_service
import time
import json
from datetime import datetime

sse_bp = Blueprint('sse', __name__)

@sse_bp.route('/<token>')
def stream(token):
    def event_stream():
        # Keep track of the last state to only send updates when changed
        last_state = None
        while True:
            session = payment_service.get_session(token)
            if not session:
                yield f"data: {json.dumps({'error': 'Invalid session'})}\n\n"
                break
                
            current_state = session.state
            if current_state != last_state:
                last_state = current_state
                payload = {
                    'state': current_state,
                    'is_final': current_state in ['SUCCESS', 'FAILED', 'CANCELLED', 'UNKNOWN', 'EXPIRED']
                }
                
                if payload['is_final']:
                    tx = session.transactions[0] if session.transactions else None
                    if tx:
                        payload['return_url'] = tx.return_url
                
                yield f"data: {json.dumps(payload)}\n\n"
                
                if payload['is_final']:
                    break
            
            # Simple polling sleep if no events system is used (gevent safe)
            # In a heavy system, Redis Pub/Sub would be used to trigger events instantly.
            # For simplicity without Redis, gevent.sleep or time.sleep works. 
            # In Gunicorn + gevent, time.sleep is monkey-patched to be non-blocking.
            time.sleep(1)
            
    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")
