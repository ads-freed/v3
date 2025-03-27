import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
socketio = SocketIO(app)

# Ensure upload and log directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'logs'), exist_ok=True)

if not app.debug:
    file_handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

# Register blueprints
from blueprints.auth import auth_bp
from blueprints.dashboard import dashboard_bp
from blueprints.tickets import tickets_bp
from blueprints.messaging import messaging_bp
from blueprints.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(tickets_bp)
app.register_blueprint(messaging_bp)
app.register_blueprint(admin_bp)

return app

# Import models so that migrations work correctly.
from models import User, Ticket, TicketReply, Message, Notification

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Only run the app if this file is executed directly.
if __name__ == '__main__':
    app = create_app()
    socketio.run(app)
