from pathlib import Path
from dotenv import dotenv_values

# Assuming your .env is in the backend folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # app/database -> backend
ENV_PATH = BASE_DIR / ".env"

env = dotenv_values(ENV_PATH, encoding="utf-8-sig")  # utf-8-sig works if BOM exists

# Print values
print(f"DB_USER: {env.get('POSTGRES_USER')}")
print(f"DB_PASSWORD: {env.get('POSTGRES_PASSWORD', '')}")
print(f"DB_HOST: {env.get('POSTGRES_SERVER')}")
print(f"DB_PORT: {env.get('POSTGRES_PORT')}")
print(f"DB_NAME: {env.get('POSTGRES_DB')}")
print(f"SECRET_KEY: {'*' * len(env.get('SECRET_KEY', ''))}")
print(f"HF_API_KEY: {env.get('HF_API_KEY')}")
