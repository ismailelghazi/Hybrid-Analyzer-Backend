from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import dotenv_values
from pathlib import Path
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.database.base import Base

# --- Load .env ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = dotenv_values(BASE_DIR / ".env")

DB_USER = env.get("POSTGRES_USER")
DB_PASS = env.get("POSTGRES_PASSWORD")
DB_HOST = env.get("POSTGRES_SERVER", "localhost")
DB_PORT = env.get("POSTGRES_PORT", "5432")
DB_NAME = env.get("POSTGRES_DB")

if not DB_USER or not DB_PASS or not DB_NAME:
    raise ValueError(f"POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB must be defined! {env}")

DB_PASS_ENCODED = quote_plus(DB_PASS)
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Create DB if not exists ---
try:
    # Connect to default postgres database
    conn = psycopg2.connect(
        dbname="postgres", user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Database '{DB_NAME}' created.")
    else:
        print(f"ℹ Database '{DB_NAME}' already exists.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Could not create/check database: {e}")
    raise

# --- SQLAlchemy setup ---
engine = create_engine(DATABASE_URL, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
