# procurement_app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-that-should-be-more-complex-in-prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///../procurement.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add other configuration variables as needed