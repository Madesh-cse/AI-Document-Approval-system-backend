from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    organization: str
    workflow_domain: str
    role: UserRole
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool

    model_config = {
        "from_attributes": True,
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse