from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    role: str


class UserCreate(UserBase):
    password: str
    role: str = "user"


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None


class UserRead(UserBase):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
