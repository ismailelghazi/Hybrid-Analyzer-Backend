"""
Database Connection Module
Supports both local PostgreSQL and Neon (via DATABASE_URL)
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv
from app.database.base import Base

# Load environment variables
load_dotenv()

# Check for DATABASE_URL first (Neon/Vercel format)
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Neon/Vercel: Use DATABASE_URL directly
    # Convert postgres:// to postgresql:// if needed (Neon uses postgres://)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Add SSL requirement for Neon
    if "sslmode" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"
    
    print("✅ Using DATABASE_URL (Neon/Cloud)")
else:
    # Local development: Build URL from individual vars
    DB_USER = os.environ.get("POSTGRES_USER")
    DB_PASS = os.environ.get("POSTGRES_PASSWORD")
    DB_HOST = os.environ.get("POSTGRES_SERVER", "localhost")
    DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
    DB_NAME = os.environ.get("POSTGRES_DB")
    
    if not DB_USER or not DB_PASS or not DB_NAME:
        raise ValueError("Database credentials not configured! Set DATABASE_URL or POSTGRES_* vars")
    
    DB_PASS_ENCODED = quote_plus(DB_PASS)
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Only try to create database locally (not in serverless)
    if os.environ.get("VERCEL") != "1":
        try:
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
            
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
    
    print("✅ Using local PostgreSQL")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, future=True, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """Dependency for routes - yields a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
