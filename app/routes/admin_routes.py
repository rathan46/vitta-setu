from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.repositories import user_repo, transaction_repo

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard.index'))

@admin_bp.route('/')
def index():
    users = user_repo.get_all()
    transactions = transaction_repo.get_all()
    return render_template('dashboard/admin_index.html', users=users, tx_count=len(transactions))
