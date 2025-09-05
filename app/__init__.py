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

    # ✅ Jinja filter to always force Cloudinary PDFs to download
    @app.template_filter('force_pdf_download')
    def force_pdf_download(url, filename=None):
        if not url:
            return url

        # Convert /raw/upload/ → /image/upload/
        if "/raw/upload/" in url:
            url = url.replace("/raw/upload/", "/image/upload/")

        if "/upload/" in url:
            # Ensure a safe filename with .pdf extension
            safe_name = filename if filename and filename.endswith(".pdf") else f"{filename or 'Noteopedia'}.pdf"

            # Add forced download transformation
            url = url.replace("/upload/", f"/upload/fl_attachment:{safe_name}/")
            
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
