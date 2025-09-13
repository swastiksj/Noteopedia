import os
import cloudinary
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()  # Load .env file for local development

from .config import Config  # Updated Config class

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.admin_login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load config

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Cloudinary configuration (only if credentials are available)
    if app.config['CLOUDINARY_CLOUD_NAME'] and app.config['CLOUDINARY_API_KEY']:
        cloudinary.config(
            cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=app.config['CLOUDINARY_API_KEY'],
            api_secret=app.config['CLOUDINARY_API_SECRET']
        )

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    # Setup database + local uploads
    with app.app_context():
        # Create all tables (works for SQLite locally & PostgreSQL on Render)
        db.create_all()

        # Only create upload folder if using SQLite/local dev
        if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

    return app
