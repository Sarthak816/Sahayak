import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional
from pathlib import Path

# Fix: Go three levels up to reach project root
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
print(f"Looking for .env at: {env_path}")  # Debug line
load_dotenv(dotenv_path=env_path)

# Debug: Print environment variables to verify

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()
security = HTTPBearer()

# Pydantic Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    new_password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    username: Optional[str] = None

# Helper Functions
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and get current user"""
    token = credentials.credentials
    
    try:
        # Verify token with Supabase
        user = supabase.auth.get_user(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        
        # Get user profile from public.profiles table
        profile = supabase.table('profiles').select('*').eq('id', user.user.id).single().execute()
        
        return {
            "id": user.user.id,
            "email": user.user.email,
            "name": profile.data.get('name') if profile.data else None,
            "username": profile.data.get('username') if profile.data else None,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
        )

# Routes
@router.post("/register", response_model=Token)
async def register(user: UserRegister):
    """Register a new user with Supabase"""
    try:
        # Sign up user with Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed"
            )
        
        # Create user profile in public.profiles table
        profile_data = {
            "id": auth_response.user.id,
            "email": user.email,
            "name": user.name,
            "username": user.username,
        }
        
        supabase.table('profiles').insert(profile_data).execute()
        
        return {
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "name": user.name,
                "username": user.username,
            }
        }
        
    except Exception as e:
        error_message = str(e)
        if "already registered" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {error_message}"
        )

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """Login with email and password using Supabase"""
    try:
        # Sign in with Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password,
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Get user profile
        profile = supabase.table('profiles').select('*').eq('id', auth_response.user.id).single().execute()
        
        return {
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "name": profile.data.get('name') if profile.data else None,
                "username": profile.data.get('username') if profile.data else None,
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token"""
    try:
        auth_response = supabase.auth.refresh_session(refresh_token)
        
        if not auth_response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        return {
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token refresh failed: {str(e)}"
        )

@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest):
    """Send password reset email via Supabase"""
    try:
        supabase.auth.reset_password_email(request.email)
        return {
            "message": "If the email exists, a password reset link has been sent"
        }
    except Exception as e:
        # Don't reveal if email exists
        return {
            "message": "If the email exists, a password reset link has been sent"
        }

@router.post("/reset-password")
async def reset_password(
    reset: PasswordReset,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Reset password (requires valid reset token)"""
    try:
        token = credentials.credentials
        
        # Update password
        supabase.auth.update_user(
            token,
            {"password": reset.new_password}
        )
        
        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password reset failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user"""
    return current_user

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user (invalidate session)"""
    try:
        token = credentials.credentials
        supabase.auth.sign_out(token)
        return {"message": "Logged out successfully"}
    except Exception as e:
        # Even if it fails, consider it logged out on client side
        return {"message": "Logged out successfully"}
