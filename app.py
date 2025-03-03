# app.py
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from config.py

# Initialize database
db = SQLAlchemy(app)

# Define database models (example: User model)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# API URLs
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    news_data = None
    city = None
    news_query = "technology"  # Default news category
    selected_section = None  # Track which section the user selected
    news_searched = False  # Track if a news search has been performed

    if request.method == "POST":
        if "select_weather" in request.form:
            selected_section = "weather"
        elif "select_news" in request.form:
            selected_section = "news"
        elif "weather_search" in request.form:
            city = request.form.get("city", "").strip()
            if city:
                weather_data = get_weather(city)
                selected_section = "weather"
        elif "news_search" in request.form:
            news_query = request.form.get("news_query", "").strip()
            if news_query:
                news_data = get_news(news_query)
                selected_section = "news"
                news_searched = True  # Mark that a news search has been performed

    return render_template(
        "index.html",
        weather_data=weather_data,
        news_data=news_data,
        city=city,
        news_query=news_query,
        selected_section=selected_section,
        news_searched=news_searched
    )

# Function to fetch weather data
def get_weather(city):
    params = {
        "q": city,
        "appid": app.config['OPENWEATHER_API_KEY'],
        "units": "metric"
    }
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Weather API request failed for {city}: {e}")
        return None

# Function to fetch news data
def get_news(query):
    params = {
        "q": query,
        "apiKey": app.config['NEWSAPI_API_KEY'],
        "pageSize": 10  # Number of articles to fetch
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"ERROR: News API request failed for {query}: {e}")
        return None

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)