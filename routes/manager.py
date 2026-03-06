from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import User, Leave
from datetime import datetime

manager_bp = Blueprint('manager', __name__)

def manager_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'manager':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@manager_bp.route('/manager/dashboard')
@manager_required
def dashboard():
    pending_leaves = Leave.get_all_pending()
    all_leaves = Leave.get_all()
    return render_template('manager_dashboard.html', pending_leaves=pending_leaves, all_leaves=all_leaves)

@manager_bp.route('/manager/leave/<int:leave_id>/approve', methods=['POST'])
@manager_required
def approve_leave(leave_id):
    data = request.get_json() if request.is_json else request.form
    comment = data.get('comment', '')
    
    leave = Leave.get_by_id(leave_id)
    if leave:
        user = User.get_by_id(leave['user_id'])
        
        # Handle date parsing for both string and date objects
        start_date = leave['start_date']
        end_date = leave['end_date']
        
        if isinstance(start_date, str):
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            start = start_date
            end = end_date
            
        days = (end - start).days + 1
        
        if leave['leave_type'] == 'Vacation':
            new_balance = user['vacation_balance'] - days
            User.update_balance(user['id'], new_balance, user['sick_balance'])
        elif leave['leave_type'] == 'Sick':
            new_balance = user['sick_balance'] - days
            User.update_balance(user['id'], user['vacation_balance'], new_balance)
        
        Leave.update_status(leave_id, 'approved', comment)
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Leave approved'})
        flash('Leave approved successfully', 'success')
    
    return redirect(url_for('manager.dashboard'))

@manager_bp.route('/manager/leave/<int:leave_id>/reject', methods=['POST'])
@manager_required
def reject_leave(leave_id):
    data = request.get_json() if request.is_json else request.form
    comment = data.get('comment', '')
    
    Leave.update_status(leave_id, 'rejected', comment)
    
    if request.is_json:
        return jsonify({'success': True, 'message': 'Leave rejected'})
    flash('Leave rejected', 'success')
    return redirect(url_for('manager.dashboard'))

@manager_bp.route('/manager/api/leaves')
@manager_required
def api_leaves():
    leaves = Leave.get_all()
    return jsonify([{
        'id': l['id'],
        'name': l['name'],
        'leave_type': l['leave_type'],
        'start_date': l['start_date'].strftime('%Y-%m-%d'),
        'end_date': l['end_date'].strftime('%Y-%m-%d'),
        'status': l['status'],
        'reason': l['reason']
    } for l in leaves])
