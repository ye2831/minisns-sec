import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_me_jwt")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VULNERABLE_MODE = os.getenv("VULNERABLE_MODE", "true").lower() in ("1","true","yes")
