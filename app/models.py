from . import db
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Increased length for hashed passwords

# Note Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)  # Cloudinary file URL
    public_id = db.Column(db.String(200), nullable=True)   # Cloudinary public_id for deletion
    level = db.Column(db.String(100), nullable=True)       # e.g., Class 10, Degree, etc.
    type = db.Column(db.String(100), nullable=True)        # e.g., Notes, Question Paper, etc.
    download_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Contact Form Submissions
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
