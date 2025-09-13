import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "this_should_be_secret")

    # Prefer PostgreSQL (Render sets DATABASE_URL), fallback to SQLite for local dev
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///notes.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cloudinary credentials (must be set in Render Environment Variables)
    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "your_cloud_name")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", "your_api_key")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "your_api_secret")

    # Google Gemini API Key (from env var, fallback only for local testing)
    GOOGLE_GEMINI_API_KEY = os.environ.get("GOOGLE_GEMINI_API_KEY", "your_fallback_gemini_key")

    # Local uploads folder (only used in dev; not needed on Render since files go to Cloudinary)
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
