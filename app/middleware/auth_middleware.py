from functools import wraps
from flask import request, jsonify
from app.services import api_key_service

def require_api_key(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
            
        public_key = auth_header.split(' ')[1]
        api_key = api_key_service.validate_public_key(public_key)
        
        if not api_key:
            return jsonify({'error': 'Invalid API Key'}), 401
            
        # Attach merchant to request
        request.merchant = api_key.user
        return f(*args, **kwargs)
    return wrapped
