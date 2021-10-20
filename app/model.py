from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, timezone


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "Lorem Lepsum !, lorem lepsum Lorem Lepsum  lorem lepsum lorem lepsum,  lorem lepsum?  lorem lepsum"
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    token: str = ""

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }
        schema_extra = {
            "example": {
                "fullname": "Abdellah Allali",
                "username": "admin",
                "email": "contact@allali.me",
                "password": "rooter"
            }
        }


class UserLoginSchema(BaseModel):
    password: str = Field(...)
    username: str = ield(...)

    class Config:
        schema_extra = {
            "example": {
                "user": "rooter",
                "password": "rooter"
            }
        }
