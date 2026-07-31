from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.auth_manager import register_user, authenticate_user, create_access_token, get_user_by_email

router = APIRouter(prefix="/auth", tags=["Authentication"])

class SignUpRequest(BaseModel):
    name: str
    email: str
    password: str

class SignInRequest(BaseModel):
    email: str
    password: str

class OAuthRequest(BaseModel):
    email: str
    name: Optional[str] = None

@router.post("/signup")
def signup(request: SignUpRequest):
    success, result = register_user(request.email, request.name, request.password, "local")
    if not success:
        raise HTTPException(status_code=400, detail=result)
    
    token = create_access_token({"sub": request.email, "name": request.name})
    return {"success": True, "token": token, "email": request.email}

@router.post("/signin")
def signin(request: SignInRequest):
    success, result = authenticate_user(request.email, request.password)
    if not success:
        raise HTTPException(status_code=401, detail=result)
    
    token = create_access_token({"sub": result["email"], "name": result["name"]})
    return {"success": True, "token": token, "email": result["email"]}

import os
import httpx
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Google OAuth Configuration
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google/callback"
GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

# GitHub OAuth Configuration
GITHUB_REDIRECT_URI = "http://localhost:8000/auth/github/callback"
GITHUB_AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USERINFO_URL = "https://api.github.com/user"
GITHUB_EMAILS_URL = "https://api.github.com/user/emails"

@router.get("/google/login")
def google_login():
    url = f"{GOOGLE_AUTHORIZATION_URL}?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20email%20profile"
    return RedirectResponse(url)

@router.get("/google/callback")
async def google_callback(code: str):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            return RedirectResponse(f"{FRONTEND_URL}/login?error=GoogleAuthFailed")

        user_response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_response.json()
        email = user_data.get("email")
        name = user_data.get("name", email.split("@")[0])
        
        user = get_user_by_email(email)
        if not user:
            success, result = register_user(email, name, None, "google")
            if not success:
                return RedirectResponse(f"{FRONTEND_URL}/login?error=RegistrationFailed")
            user = result
            
        jwt_token = create_access_token({"sub": user["email"], "name": user["name"]})
        return RedirectResponse(f"{FRONTEND_URL}/?token={jwt_token}&email={user['email']}")

@router.get("/github/login")
def github_login():
    url = f"{GITHUB_AUTHORIZATION_URL}?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=user:email"
    return RedirectResponse(url)

@router.get("/github/callback")
async def github_callback(code: str):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI,
            },
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            return RedirectResponse(f"{FRONTEND_URL}/login?error=GithubAuthFailed")

        # Get user info
        user_response = await client.get(
            GITHUB_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_response.json()
        name = user_data.get("name") or user_data.get("login")
        
        # Get user email
        emails_response = await client.get(
            GITHUB_EMAILS_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        emails = emails_response.json()
        primary_email = next((e["email"] for e in emails if e["primary"]), None)
        
        if not primary_email:
            return RedirectResponse(f"{FRONTEND_URL}/login?error=GithubNoEmail")

        user = get_user_by_email(primary_email)
        if not user:
            success, result = register_user(primary_email, name, None, "github")
            if not success:
                return RedirectResponse(f"{FRONTEND_URL}/login?error=RegistrationFailed")
            user = result
            
        jwt_token = create_access_token({"sub": user["email"], "name": user["name"]})
        return RedirectResponse(f"{FRONTEND_URL}/?token={jwt_token}&email={user['email']}")
