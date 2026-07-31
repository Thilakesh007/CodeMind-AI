import os
import hashlib
import jwt
import datetime
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine, Base
from app.models import User

Base.metadata.create_all(bind=engine)

SECRET_KEY = "super_secret_jwt_key_for_codemind_ai"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 1 week

def get_password_hash(password: str) -> str:
    salt = b"codemind_salt"
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return hashed.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def register_user(email: str, name: str, password: str = None, auth_provider: str = "local"):
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.email == email).first()
        if db_user:
            return False, "Email already registered"
        
        hashed_password = get_password_hash(password) if password else None
        
        new_user = User(
            email=email,
            name=name,
            hashed_password=hashed_password,
            auth_provider=auth_provider
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return True, {
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name,
            "auth_provider": new_user.auth_provider
        }
    finally:
        db.close()

def authenticate_user(email: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False, "User not found"
        
        if user.auth_provider != "local":
            return False, f"Please sign in with {user.auth_provider} instead."
            
        if not verify_password(password, user.hashed_password):
            return False, "Incorrect password"
            
        return True, {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    finally:
        db.close()

def get_user_by_email(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "auth_provider": user.auth_provider
            }
        return None
    finally:
        db.close()
