from sqlalchemy import String, Text, Enum, ForeignKey
from datetime import datetime, date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from enum import Enum as PyEnum
from typing import List


# Enums
class Gender(PyEnum):
    MALE = "male"
    FEMALE = "female"
    NOT_SPECIFIED = "not_specified"


# Models
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)
    profile_pic: Mapped[str] = mapped_column(String(255), nullable=True)
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
    reviews: Mapped[List['Review']] = relationship(back_populates="user")

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


class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rate: Mapped[float] = mapped_column(nullable=False, default=1.0)
    duration: Mapped[float] = mapped_column(nullable=False)
    release_year: Mapped[int] = mapped_column(nullable=False)
    cover: Mapped[str] = mapped_column(String(255), nullable=False)
    countries: Mapped[list[str]] = mapped_column(nullable=False)
    languages: Mapped[list[str]] = mapped_column(nullable=False)
    director: Mapped[str] = mapped_column(nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    storyline: Mapped[str] = mapped_column(Text, nullable=False)
    budget: Mapped[float] = mapped_column(nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Cast(Base):
    __tablename__ = 'casts'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)
    profile_pic: Mapped[str] = mapped_column(String(255), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    dob: Mapped[date] = mapped_column(nullable=True)
    gender: Mapped[Gender] = mapped_column(
        nullable=True, default=Gender.NOT_SPECIFIED)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Writer(Base):
    __tablename__ = 'writers'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)
    profile_pic: Mapped[str] = mapped_column(String(255), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    dob: Mapped[date] = mapped_column(nullable=True)
    gender: Mapped[Gender] = mapped_column(
        nullable=True, default=Gender.NOT_SPECIFIED)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    rate: Mapped[int] = mapped_column(Enum(1, 2, 3, 4, 5), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    user: Mapped[User] = relationship(back_populates="reviews")
