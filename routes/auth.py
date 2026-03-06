from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if 'user_id' in session:
        if session['role'] == 'manager':
            return redirect(url_for('manager.dashboard'))
        return redirect(url_for('employee.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'employee')
        department = data.get('department')

        if User.find_by_email(email):
            if request.is_json:
                return jsonify({'success': False, 'message': 'Email already exists'}), 400
            flash('Email already exists', 'error')
            return redirect(url_for('auth.register'))

        User.create(name, email, password, role, department)
        if request.is_json:
            return jsonify({'success': True, 'message': 'Registration successful'})
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')

        user = User.find_by_email(email)
        if user and User.verify_password(user['password'], password):
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']
            session['email'] = user['email']
            
            if request.is_json:
                return jsonify({'success': True, 'role': user['role']})
            
            if user['role'] == 'manager':
                return redirect(url_for('manager.dashboard'))
            return redirect(url_for('employee.dashboard'))

        if request.is_json:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        flash('Invalid email or password', 'error')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))
