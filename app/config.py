# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # .env 읽기

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "devjwtsecret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_ENV") == "development" or os.getenv("FLASK_DEBUG") == "1"
