from sqlalchemy import String, Boolean, Integer, Column, Enum, ForeignKey, DateTime
from datetime import datetime, date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from enum import Enum as PyEnum
from typing import List


# Enums
class ListingType(PyEnum):
    HOUSE = "house"
    APARTMENT = "apartment"


class Gender(PyEnum):
    MALE = "male"
    FEMALE = "female"
    NOT_SPECIFIED = "not_specified"


# Models
class Listing(Base):
    __tablename__ = 'listings'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    type: Mapped[ListingType] = mapped_column(nullable=False)
    availableNow: Mapped[bool] = mapped_column(nullable=False, default=True)
    ownerId: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    address: Mapped[str] = mapped_column(String(1000), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    owner: Mapped["User"] = relationship(back_populates="listings")


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    userName: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    fullName: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    hashedPassword: Mapped[str] = mapped_column(String(255), nullable=False)
    dob: Mapped[date] = mapped_column(nullable=True)
    gender: Mapped[Gender] = mapped_column(
        nullable=True, default=Gender.NOT_SPECIFIED)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    listings: Mapped[List[Listing]] = relationship(back_populates="owner")

    @classmethod
    async def validate_dob(cls, dob_str):
        # Validate date format
        try:
            dob = datetime.strptime(dob_str, "%d-%m-%Y").date()
        except ValueError:
            return False, "Invalid date format. Date should be in dd-mm-YYYY format."

        # Validate minimum year
        if dob.year <= 1940:
            return False, "Year of birth should be after 1940."

        return True, dob
