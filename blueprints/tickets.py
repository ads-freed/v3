import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import Ticket, TicketAttachment, TicketReply, ReplyAttachment
from forms import TicketForm, TicketReplyForm
from extensions import db, socketio

tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@tickets_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, description=form.description.data, user_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        ticket.generate_ticket_number()
        db.session.commit()
        # Handle file attachment
        file = request.files.get('attachment')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.utcnow().timestamp()}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
            attachment = TicketAttachment(filename=unique_filename, ticket_id=ticket.id)
            db.session.add(attachment)
            db.session.commit()
        # Emit real‑time notification
        socketio.emit('ticket_notification', {'message': 'New ticket created', 'ticket_id': ticket.id})
        flash('Ticket created successfully!')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('ticket_create.html', form=form)

@tickets_bp.route('/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = TicketReplyForm()
    if form.validate_on_submit():
        reply = TicketReply(content=form.content.data, user_id=current_user.id, ticket_id=ticket.id)
        db.session.add(reply)
        db.session.commit()
        # Handle reply attachment
        file = request.files.get('attachment')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.utcnow().timestamp()}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
            attachment = ReplyAttachment(filename=unique_filename, reply_id=reply.id)
            db.session.add(attachment)
            db.session.commit()
        socketio.emit('ticket_notification', {'message': 'New reply added', 'ticket_id': ticket.id})
        flash('Reply submitted successfully!')
        return redirect(url_for('tickets.ticket_detail', ticket_id=ticket.id))
    return render_template('ticket_detail.html', ticket=ticket, form=form)

@tickets_bp.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
