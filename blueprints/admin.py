from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from models import User, Ticket
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access required')
            return redirect(url_for('dashboard.dashboard'))
        return func(*args, **kwargs)
    return decorated_view

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/tickets')
@login_required
@admin_required
def manage_tickets():
    tickets = Ticket.query.all()
    return render_template('admin_tickets.html', tickets=tickets)

@admin_bp.route('/logs')
@login_required
@admin_required
def view_logs():
    log_file = current_app.config['LOG_FILE']
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = f.read()
    else:
        logs = "No logs available."
    return render_template('logs.html', logs=logs)
