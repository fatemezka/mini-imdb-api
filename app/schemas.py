from pydantic import BaseModel, validator
from typing import Optional
from app.models import Gender, ListingType
from datetime import date, datetime
from app.utils.error_handler import ErrorHandler


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


class IUpdateUserBody(BaseModel):
    username: str
    email: str
    password: Optional[str] = None
    fullname: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[Gender] = None


class IUpdateUserController(BaseModel):
    username: str
    email: str
    hashedPassword: str
    fullname: Optional[str] = None
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
