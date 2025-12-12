from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app.database.connection import get_db, engine
from app.database.base import Base
from app.models.user import User  # Import to register model with Base
from app.schemas.user_schema import UserCreate, UserLogin, UserOut
from app.services.auth_service import create_user, authenticate_user
from app.utils.security import create_access_token, decode_token

router = APIRouter()

# create tables (for dev). In prod use migrations
Base.metadata.create_all(bind=engine)

COOKIE_NAME = "access_token"


def _user_to_dict(user: User) -> dict:
    """Convert user to dict for response"""
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }


@router.post("/register")
def register(payload: UserCreate, response: Response, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, payload.email, payload.password)
    
    # Create token for the new user
    token = create_access_token({"sub": str(user.id), "email": user.email})
    
    # Set cookie as fallback
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=60 * 60 * 24,  # 1 day
        samesite="none",
        secure=True,
        path="/"
    )
    
    # Return token in response body for cross-origin support
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": _user_to_dict(user)
    }


@router.post("/login")
def login(payload: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "email": user.email})
    
    # Set cookie as fallback with cross-origin support
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=60 * 60 * 24,  # 1 day
        samesite="none",
        secure=True,
        path="/"
    )
    
    # Return token in response body for cross-origin support
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": _user_to_dict(user)
    }


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = None
    
    # First, try to get token from Authorization header (Bearer token)
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Remove "Bearer " prefix
    
    # Fallback to cookie if no Authorization header
    if not token:
        token = request.cookies.get(COOKIE_NAME)
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    data = decode_token(token)
    if not data or "sub" not in data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(data["sub"])
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user


@router.post("/logout")
def logout(response: Response):
    # clear cookie
    response.delete_cookie(COOKIE_NAME, path="/", samesite="none", secure=True)
    return {"message": "Logged out"}
