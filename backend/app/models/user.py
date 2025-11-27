"""
User model
"""

from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool = True
    is_superuser: bool = False
    role: Optional[str] = "student"
    
    class Config:
        from_attributes = True
