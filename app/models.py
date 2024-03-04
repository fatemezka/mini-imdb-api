from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime, date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from enum import Enum as PyEnum
from typing import List


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
    countries = mapped_column(ARRAY(String), nullable=False)
    languages = mapped_column(ARRAY(String), nullable=False)
    director: Mapped[str] = mapped_column(nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    storyline: Mapped[str] = mapped_column(Text, nullable=False)
    budget: Mapped[float] = mapped_column(nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movie_cast: Mapped['MovieCast'] = relationship(back_populates="movie")
    movie_writer: Mapped['MovieWriter'] = relationship(back_populates="movie")
    movie_genre: Mapped['MovieGenre'] = relationship(back_populates="movie")


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

    # relations
    movie_cast: Mapped['MovieCast'] = relationship(back_populates="cast")


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

    # relations
    movie_writer: Mapped['MovieWriter'] = relationship(back_populates="writer")


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movie_genre: Mapped['MovieGenre'] = relationship(back_populates="genre")


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
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
    cast_id: Mapped[int] = mapped_column(
        ForeignKey("casts.id"), nullable=False)
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id"), nullable=False)
    star: Mapped[bool] = mapped_column(nullable=False, default=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movie: Mapped[Movie] = relationship(back_populates="movie_cast")
    cast: Mapped[Cast] = relationship(back_populates="movie_cast")


class MovieWriter(Base):
    __tablename__ = 'movie_writers'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    writer_id: Mapped[int] = mapped_column(
        ForeignKey("writers.id"), nullable=False)
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id"), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movie: Mapped[Movie] = relationship(back_populates="movie_writer")
    writer: Mapped[Writer] = relationship(back_populates="movie_writer")


class MovieGenre(Base):
    __tablename__ = 'movie_genres'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.id"), nullable=False)
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id"), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    movie: Mapped[Movie] = relationship(back_populates="movie_genre")
    genre: Mapped[Genre] = relationship(back_populates="movie_genre")
