from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta

# Simple in-memory rate limiting for demonstration.
# In production, this should be backed by Redis.
_rate_limits = {}

def rate_limit(limit=100, per=60):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ip = request.remote_addr
            now = datetime.utcnow()
            
            if ip not in _rate_limits:
                _rate_limits[ip] = []
            
            # Remove old requests
            _rate_limits[ip] = [t for t in _rate_limits[ip] if t > now - timedelta(seconds=per)]
            
            if len(_rate_limits[ip]) >= limit:
                return jsonify({'error': 'Rate limit exceeded'}), 429
                
            _rate_limits[ip].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator
