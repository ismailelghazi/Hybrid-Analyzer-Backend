"""
Authentication Endpoint Tests
Tests for /auth/register, /auth/login, /auth/me, /auth/logout
"""
import pytest


class TestRegister:
    """Tests for POST /auth/register"""
    
    def test_register_success(self, client, test_user_data):
        """Test successful user registration"""
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == test_user_data["email"]
        assert data["user"]["id"] is not None
    
    def test_register_duplicate_email(self, client, test_user_data):
        """Test registration fails with duplicate email"""
        # First registration
        client.post("/auth/register", json=test_user_data)
        
        # Second registration with same email
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_invalid_email(self, client):
        """Test registration fails with invalid email format"""
        response = client.post("/auth/register", json={
            "email": "invalid-email",
            "password": "testpassword123"
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_register_missing_password(self, client):
        """Test registration fails with missing password"""
        response = client.post("/auth/register", json={
            "email": "test@example.com"
        })
        
        assert response.status_code == 422  # Validation error


class TestLogin:
    """Tests for POST /auth/login"""
    
    def test_login_success(self, client, test_user_data):
        """Test successful login"""
        # Register first
        client.post("/auth/register", json=test_user_data)
        
        # Login
        response = client.post("/auth/login", json=test_user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == test_user_data["email"]
    
    def test_login_wrong_password(self, client, test_user_data):
        """Test login fails with wrong password"""
        # Register first
        client.post("/auth/register", json=test_user_data)
        
        # Login with wrong password
        response = client.post("/auth/login", json={
            "email": test_user_data["email"],
            "password": "wrongpassword"
        })
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client):
        """Test login fails for non-existent user"""
        response = client.post("/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "testpassword123"
        })
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]


class TestMe:
    """Tests for GET /auth/me"""
    
    def test_me_authenticated(self, client, auth_headers, test_user_data):
        """Test getting current user when authenticated"""
        response = client.get("/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert "id" in data
        assert "created_at" in data
    
    def test_me_no_token(self, client):
        """Test /auth/me fails without token"""
        response = client.get("/auth/me")
        
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
    
    def test_me_invalid_token(self, client):
        """Test /auth/me fails with invalid token"""
        response = client.get("/auth/me", headers={
            "Authorization": "Bearer invalid_token_here"
        })
        
        assert response.status_code == 401


class TestLogout:
    """Tests for POST /auth/logout"""
    
    def test_logout_success(self, client, auth_headers):
        """Test successful logout"""
        response = client.post("/auth/logout", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Logged out"
