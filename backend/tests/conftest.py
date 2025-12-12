"""
Pytest Configuration and Test Fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.database.base import Base
from app.database.connection import get_db
from app.models.user import User


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Test client with database override"""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }


@pytest.fixture
def auth_headers(client, test_user_data):
    """Get authentication headers for protected endpoints"""
    # Register user
    client.post("/auth/register", json=test_user_data)
    
    # Login to get token
    response = client.post("/auth/login", json=test_user_data)
    token = response.json().get("access_token")
    
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_huggingface_response():
    """Mock successful HuggingFace API response"""
    return {
        "category": "technology",
        "confidence": 0.8912,
        "scores": {
            "technology": 0.8912,
            "business": 0.0654,
            "science": 0.0321,
            "politics": 0.0058,
            "entertainment": 0.0034,
            "health": 0.0012,
            "sports": 0.0005,
            "education": 0.0002,
            "travel": 0.0001,
            "food": 0.0001
        },
        "latency_ms": 450
    }


@pytest.fixture
def mock_gemini_response():
    """Mock successful Gemini API response"""
    return {
        "summary": "This text discusses technological innovations and their impact on modern society.",
        "tone": "positif",
        "latency_ms": 650
    }


@pytest.fixture
def sample_text():
    """Sample text for analysis testing"""
    return "The new artificial intelligence system has revolutionized the way we process data. " \
           "Machine learning algorithms are now capable of analyzing complex patterns and making " \
           "predictions with unprecedented accuracy. This technological breakthrough promises to " \
           "transform industries from healthcare to finance."
