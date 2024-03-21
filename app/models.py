from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime, date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from enum import Enum as PyEnum
from typing import List
import os


# Enums
class Gender(PyEnum):
    MALE = "male"
    FEMALE = "female"
    NOT_SPECIFIED = "not_specified"


class ReviewRate(PyEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


# Models
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)
    profilePic: Mapped[str] = mapped_column(String(255), nullable=True)
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
        MINIMUM_USER_BIRTH_YEAR = os.environ.get('MINIMUM_USER_BIRTH_YEAR')
        if dob.year <= MINIMUM_USER_BIRTH_YEAR:
            return False, f"Year of birth should be after {MINIMUM_USER_BIRTH_YEAR}."

        return True, dob


class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rate: Mapped[float] = mapped_column(nullable=False, default=1.0)
    duration: Mapped[float] = mapped_column(nullable=False)
    releaseYear: Mapped[int] = mapped_column(nullable=False)
    cover: Mapped[str] = mapped_column(String(255), nullable=False)
    countries = mapped_column(ARRAY(String), nullable=False)
    languages = mapped_column(ARRAY(String), nullable=False)
    director: Mapped[str] = mapped_column(nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    storyline: Mapped[str] = mapped_column(Text, nullable=False)
    budget: Mapped[float] = mapped_column(nullable=False)  # based on dollar
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movieCast: Mapped['MovieCast'] = relationship(back_populates="movie")
    movieWriter: Mapped['MovieWriter'] = relationship(back_populates="movie")
    movieGenre: Mapped['MovieGenre'] = relationship(back_populates="movie")


class Cast(Base):
    __tablename__ = 'casts'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)
    profilePic: Mapped[str] = mapped_column(String(255), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    dob: Mapped[date] = mapped_column(nullable=True)
    gender: Mapped[Gender] = mapped_column(
        nullable=True, default=Gender.NOT_SPECIFIED)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movieCast: Mapped['MovieCast'] = relationship(back_populates="cast")


class Writer(Base):
    __tablename__ = 'writers'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)
    profilePic: Mapped[str] = mapped_column(String(255), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    dob: Mapped[date] = mapped_column(nullable=True)
    gender: Mapped[Gender] = mapped_column(
        nullable=True, default=Gender.NOT_SPECIFIED)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movieWriter: Mapped['MovieWriter'] = relationship(back_populates="writer")


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movieGenre: Mapped['MovieGenre'] = relationship(back_populates="genre")


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    userId: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    rate: Mapped[ReviewRate] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    user: Mapped[User] = relationship(back_populates="reviews")


class MovieCast(Base):
    __tablename__ = 'movie_casts'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    castId: Mapped[int] = mapped_column(
        ForeignKey("casts.id"), nullable=False)
    movieId: Mapped[int] = mapped_column(
        ForeignKey("movies.id"), nullable=False)
    isStar: Mapped[bool] = mapped_column(nullable=False, default=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movie: Mapped[Movie] = relationship(back_populates="movieCast")
    cast: Mapped[Cast] = relationship(back_populates="movieCast")


class MovieWriter(Base):
    __tablename__ = 'movie_writers'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    writerId: Mapped[int] = mapped_column(
        ForeignKey("writers.id"), nullable=False)
    movieId: Mapped[int] = mapped_column(
        ForeignKey("movies.id"), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movie: Mapped[Movie] = relationship(back_populates="movieWriter")
    writer: Mapped[Writer] = relationship(back_populates="movieWriter")


class MovieGenre(Base):
    __tablename__ = 'movie_genres'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    genreId: Mapped[int] = mapped_column(
        ForeignKey("genres.id"), nullable=False)
    movieId: Mapped[int] = mapped_column(
        ForeignKey("movies.id"), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movie: Mapped[Movie] = relationship(back_populates="movieGenre")
    genre: Mapped[Genre] = relationship(back_populates="movieGenre")
