from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.repositories import user_repo, transaction_repo
from app.services import admin_service

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard.index'))

@admin_bp.route('/')
def index():
    stats = admin_service.get_global_stats()
    # Get last 15 global transactions
    recent_txs = transaction_repo.get_all()
    recent_txs = sorted(recent_txs, key=lambda x: x.created_time, reverse=True)[:15]
    return render_template('admin/index.html', stats=stats, transactions=recent_txs)

@admin_bp.route('/merchants')
def merchants():
    users = user_repo.get_all()
    # Filter out admins from the merchant list
    merchants = [u for u in users if not u.is_admin]
    return render_template('admin/merchants.html', merchants=merchants)

@admin_bp.route('/merchants/<int:user_id>/toggle', methods=['POST'])
def toggle_merchant(user_id):
    success, msg = admin_service.toggle_merchant_status(user_id)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')
    return redirect(url_for('admin.merchants'))

@admin_bp.route('/transactions')
def transactions():
    txs = transaction_repo.get_all()
    # Sort newest first
    txs = sorted(txs, key=lambda x: x.created_time, reverse=True)
    return render_template('admin/transactions.html', transactions=txs)
