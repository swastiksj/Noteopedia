import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "this_should_be_secret"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///notes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cloudinary credentials - get from environment variables or use defaults
    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME") or "your_cloud_name"
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY") or "your_api_key"
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET") or "your_api_secret"

    # Google Gemini API Key (avoid hardcoding in production!)
    GOOGLE_GEMINI_API_KEY = os.environ.get("GOOGLE_GEMINI_API_KEY") or "your_fallback_gemini_key"

    # Local uploads folder (used if not uploading to Cloudinary)
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
