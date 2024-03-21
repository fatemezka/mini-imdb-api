from pydantic import BaseModel
from typing import Optional
from app.models import Gender
from datetime import date


# User
class ICreateUserBody(BaseModel):
    username: str
    email: str
    password: str
    fullname: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[Gender] = None


class ICreateUserController(BaseModel):
    username: str
    email: str
    hashedPassword: str
    fullname: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[Gender] = None


class ILoginUser(BaseModel):
    username: str
    password: str
