from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Ticket

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def dashboard():
    if current_user.role in ['admin', 'support']:
        # Admin/Support view: display all tickets with statistics.
        tickets = Ticket.query.all()
        return render_template('dashboard_admin.html', tickets=tickets)
    else:
        # Customer view: only show tickets created by the current user.
        tickets = Ticket.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard_customer.html', tickets=tickets)
