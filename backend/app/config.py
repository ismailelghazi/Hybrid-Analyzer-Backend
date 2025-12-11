import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# JWT Configuration - support both naming conventions
SECRET_KEY = os.environ.get("SECRET_KEY") or os.environ.get("JWT_SECRET", "supersecretkey123")
JWT_SECRET = SECRET_KEY  # alias
ALGORITHM = os.environ.get("ALGORITHM") or os.environ.get("JWT_ALGO", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# API Keys
HF_TOKEN = os.environ.get("HF_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Mock Mode - set to "true" to use fake responses instead of real APIs
MOCK_MODE = os.environ.get("MOCK_MODE", "false").lower() == "true"

# Validation
MIN_TEXT_LENGTH = 20
