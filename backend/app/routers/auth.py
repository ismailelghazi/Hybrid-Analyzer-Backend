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

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, payload.email, payload.password)
    return user

@router.post("/login")
def login(payload: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "email": user.email})
    # set cookie; secure=False for local dev; set secure=True in production HTTPS
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=60 * 60 * 24,  # 1 day
        samesite="lax",
        secure=False,
        path="/"
    )
    return {"message": "Logged in"}

def get_current_user(request: Request, db: Session = Depends(get_db)):
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
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"message": "Logged out"}
