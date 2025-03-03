# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:ANJALI999@localhost:5432/aggregator')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    NEWSAPI_API_KEY = os.environ.get('NEWSAPI_API_KEY')