import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from app import db, socketio
from models import Message, User
from forms import MessageForm
from werkzeug.utils import secure_filename

messaging_bp = Blueprint('messaging', __name__, url_prefix='/messages')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@messaging_bp.route('/')
@login_required
def user_list():
    # List all users (except the current user) to start a private chat.
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('chat.html', users=users)

@messaging_bp.route('/chat/<int:recipient_id>', methods=['GET', 'POST'])
@login_required
def chat(recipient_id):
    recipient = User.query.get_or_404(recipient_id)
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(sender_id=current_user.id, recipient_id=recipient.id, content=form.content.data)
        file = request.files.get('attachment')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.utcnow().timestamp()}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
            message.attachment = unique_filename
        db.session.add(message)
        db.session.commit()
        socketio.emit('private_message', {'message': 'New private message', 'sender': current_user.username, 'recipient_id': recipient.id})
        flash('Message sent successfully!')
        return redirect(url_for('messaging.chat', recipient_id=recipient.id))
    # Retrieve conversation messages between the two users.
    messages = Message.query.filter(
        ((Message.sender_id==current_user.id) & (Message.recipient_id==recipient.id)) |
        ((Message.sender_id==recipient.id) & (Message.recipient_id==current_user.id))
    ).order_by(Message.created_at).all()
    return render_template('chat.html', recipient=recipient, form=form, messages=messages)

@messaging_bp.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
