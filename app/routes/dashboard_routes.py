from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services import dashboard_service, api_key_service
from app.repositories import transaction_repo, payment_session_repo
from app.extensions import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    stats = dashboard_service.get_dashboard_stats(current_user.id)
    recent_transactions = transaction_repo.get_by_merchant(current_user.id)[:10]
    return render_template('dashboard/index.html', stats=stats, transactions=recent_transactions)

@dashboard_bp.route('/transactions')
@login_required
def transactions():
    txs = transaction_repo.get_by_merchant(current_user.id)
    return render_template('dashboard/transactions.html', transactions=txs)

@dashboard_bp.route('/transaction/<tx_id>')
@login_required
def transaction_detail(tx_id):
    tx = transaction_repo.get_by_id(tx_id)
    if not tx or tx.merchant_id != current_user.id:
        return "Not found", 404
    return render_template('dashboard/transaction_detail.html', transaction=tx)

@dashboard_bp.route('/api-keys', methods=['GET', 'POST'])
@login_required
def api_keys():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'generate':
            api_key_service.generate_keys_for_user(current_user.id)
            flash('New API Key generated successfully.', 'success')
        elif action == 'revoke':
            key_id = request.form.get('key_id')
            api_key_service.revoke_key(key_id)
            flash('API Key revoked.', 'info')
        return redirect(url_for('dashboard.api_keys'))
        
    keys = api_key_service.validate_public_key(current_user.id) # using get by user in repo actually, wait
    # Let's fix this method call. api_key_repo.get_by_user_id exists
    from app.repositories import api_key_repo
    keys = api_key_repo.get_by_user_id(current_user.id)
    return render_template('dashboard/api_keys.html', keys=keys)

@dashboard_bp.route('/docs')
@login_required
def docs():
    return render_template('docs/api_docs.html')

@dashboard_bp.route('/playground')
@login_required
def playground():
    from app.repositories import api_key_repo
    keys = api_key_repo.get_by_user_id(current_user.id)
    active_key = next((k for k in keys if k.is_active), None)
    return render_template('docs/playground.html', active_key=active_key)

@dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.business_name = request.form.get('business_name', current_user.business_name)
        current_user.primary_color = request.form.get('primary_color', current_user.primary_color)
        current_user.payment_page_theme = request.form.get('payment_page_theme', current_user.payment_page_theme)
        db.session.commit()
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('dashboard.settings'))
    return render_template('dashboard/settings.html')
