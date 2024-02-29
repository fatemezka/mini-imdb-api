from pydantic import BaseModel, validator
from typing import Optional
from app.models import Gender, ListingType
from datetime import date, datetime
from app.utils.error_handler import ErrorHandler


# User
class ICreateUserBody(BaseModel):
    userName: str
    email: str
    password: str
    fullName: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[Gender] = None


class ICreateUserController(BaseModel):
    userName: str
    email: str
    hashedPassword: str
    fullName: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[Gender] = None


class ILoginUser(BaseModel):
    userName: str
    password: str


class IUpdateUserBody(BaseModel):
    userName: str
    email: str
    password: Optional[str] = None
    fullName: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[Gender] = None


class IUpdateUserController(BaseModel):
    userName: str
    email: str
    hashedPassword: str
    fullName: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[Gender] = None


# Listing
class ICreateListingBody(BaseModel):
    type: ListingType
    availableNow: bool
    address: str


class ICreateListingController(BaseModel):
    type: ListingType
    availableNow: bool
    ownerId: int
    address: str


class IUpdateListing(BaseModel):
    type: ListingType
    availableNow: bool
    address: str
