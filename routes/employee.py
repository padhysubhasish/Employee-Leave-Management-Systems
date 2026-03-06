from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import User, Leave
from datetime import datetime

employee_bp = Blueprint('employee', __name__)

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def employee_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or session.get('role') not in ['employee', 'manager']:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@employee_bp.route('/dashboard')
@login_required
@employee_required
def dashboard():
    user = User.get_by_id(session['user_id'])
    leaves = Leave.get_by_user(session['user_id'])
    return render_template('employee_dashboard.html', user=user, leaves=leaves)

@employee_bp.route('/leave/request', methods=['GET', 'POST'])
@login_required
@employee_required
def request_leave():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        leave_type = data.get('leave_type')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        reason = data.get('reason')

        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        days = (end - start).days + 1

        user = User.get_by_id(session['user_id'])
        
        if leave_type == 'Vacation' and user['vacation_balance'] < days:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Insufficient vacation balance'}), 400
            flash('Insufficient vacation balance', 'error')
            return redirect(url_for('employee.request_leave'))
        
        if leave_type == 'Sick' and user['sick_balance'] < days:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Insufficient sick leave balance'}), 400
            flash('Insufficient sick leave balance', 'error')
            return redirect(url_for('employee.request_leave'))

        Leave.create(session['user_id'], leave_type, start_date, end_date, reason)
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Leave request submitted'})
        flash('Leave request submitted successfully', 'success')
        return redirect(url_for('employee.dashboard'))

    user = User.get_by_id(session['user_id'])
    return render_template('leave_request.html', user=user)

@employee_bp.route('/leave/history')
@login_required
@employee_required
def leave_history():
    leaves = Leave.get_by_user(session['user_id'])
    return render_template('leave_history.html', leaves=leaves)

@employee_bp.route('/api/leave/calendar')
@login_required
@employee_required
def leave_calendar():
    leaves = Leave.get_approved_leaves()
    events = []
    for leave in leaves:
        events.append({
            'title': f"{leave['name']} - {leave['leave_type']}",
            'start': leave['start_date'].strftime('%Y-%m-%d'),
            'end': leave['end_date'].strftime('%Y-%m-%d')
        })
    return jsonify(events)
