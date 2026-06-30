from flask import Blueprint, jsonify
from app.extensions import db, scheduler
import json

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/health')
def health():
    status = {
        'status': 'ok',
        'database': 'unknown',
        'scheduler': 'running' if scheduler.running else 'stopped'
    }
    
    try:
        # Simple DB check
        db.session.execute(db.text('SELECT 1'))
        status['database'] = 'ok'
    except Exception as e:
        status['database'] = 'error'
        status['status'] = 'error'
        
    return jsonify(status), 200 if status['status'] == 'ok' else 500

@monitoring_bp.route('/metrics')
def metrics():
    # Placeholder for Prometheus metrics or custom JSON metrics
    return jsonify({'total_requests': 'N/A'})

@monitoring_bp.route('/version')
def version():
    return jsonify({'version': '1.0.0', 'name': 'Vitta Setu'})
