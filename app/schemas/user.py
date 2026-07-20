from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum


class UserCreate(BaseModel):
    """Schema for registering a new user — what the client sends us."""
    email: EmailStr
    password: str
    role: RoleEnum


class UserResponse(BaseModel):
    """Schema for what we send back — never includes the password."""
    id: int
    email: EmailStr
    role: RoleEnum
    is_active: bool

    class Config:
        from_attributes = True