import os
import cloudinary
import cloudinary.uploader
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

from .config import Config  # Import your updated Config class

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.admin_login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load config from config.py

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Cloudinary configuration
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )

    # ✅ Register Jinja filter to force Cloudinary links as .pdf downloads
    @app.template_filter('force_pdf_download')
    def force_pdf_download(url, filename=None):
        if not url:
            return url
        if "/upload/" in url:
            if filename:
                return url.replace("/upload/", f"/upload/fl_attachment:{filename}/")
            else:
                return url.replace("/upload/", "/upload/fl_attachment/")
        return url

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    # Ensure local upload folder exists (optional if fully Cloudinary-based)
    with app.app_context():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Optional: Create DB if it doesn't exist
        if not os.path.exists("notes.db"):
            print("Creating new database...")
            db.create_all()

    return app
