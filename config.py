import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY     = os.getenv("SECRET_KEY", "fallback-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt")

    # Database
    SQLALCHEMY_DATABASE_URI        = os.getenv("DATABASE_URL", "sqlite:///samajhher.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT — token valid for 7 days
    # Why 7 days? Unlike a cafe app, a user here may come back
    # after several days to check her saved history
    JWT_ACCESS_TOKEN_EXPIRES = 604800

    # Gemini API key
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")