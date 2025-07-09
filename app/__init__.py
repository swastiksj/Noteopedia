import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.admin_login'  # correct route

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Sourav@123'  # Use env var in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
    app.config['UPLOAD_FOLDER'] = os.path.join('app','static', 'uploads')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
 
    # Register blueprint inside the function
    from .routes import main
    app.register_blueprint(main)

    # Ensure upload folder exists
    with app.app_context():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        db.create_all()

    return app
