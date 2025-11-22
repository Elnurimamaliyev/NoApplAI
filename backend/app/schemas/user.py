"""
User schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=255)
    current_degree: Optional[str] = Field(None, max_length=100)
    current_major: Optional[str] = Field(None, max_length=100)
    gpa: Optional[str] = Field(None, max_length=10)
    bio: Optional[str] = None


class UserProfileUpdate(BaseModel):
    phone: Optional[str] = None
    location: Optional[str] = None
    current_degree: Optional[str] = None
    current_major: Optional[str] = None
    gpa: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    is_verified: bool
    phone: Optional[str]
    location: Optional[str]
    current_degree: Optional[str]
    current_major: Optional[str]
    gpa: Optional[str]
    profile_completion: str
    bio: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)
