from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.services import auth_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        success, result = auth_service.authenticate(email, password)
        if success:
            login_user(result)
            return redirect(url_for('dashboard.index'))
        else:
            flash(result, 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        merchant_name = request.form.get('merchant_name')
        owner_name = request.form.get('owner_name')
        business_name = request.form.get('business_name')
        
        success, result = auth_service.register_merchant(
            email, password, merchant_name, owner_name, business_name
        )
        if success:
            login_user(result)
            return redirect(url_for('dashboard.index'))
        else:
            flash(result, 'danger')
            
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
