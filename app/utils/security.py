import uuid
import hmac
import hashlib
import secrets
from datetime import datetime, timezone
import json

def generate_uuid():
    return str(uuid.uuid4())

def generate_api_key():
    public_key = f"pk_test_{secrets.token_hex(16)}"
    private_secret = f"sk_test_{secrets.token_hex(32)}"
    return public_key, private_secret

def generate_temporary_token():
    return secrets.token_urlsafe(32)

def generate_hmac_signature(secret, payload, timestamp):
    """Generates an HMAC SHA256 signature for callbacks."""
    message = f"{timestamp}.{json.dumps(payload, separators=(',', ':'))}"
    signature = hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_hmac_signature(secret, payload, timestamp, signature):
    expected_signature = generate_hmac_signature(secret, payload, timestamp)
    return hmac.compare_digest(expected_signature, signature)
