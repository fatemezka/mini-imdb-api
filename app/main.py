from fastapi import FastAPI
from app.db.base import create_all_tables
from app.middleware import CustomMiddleware
import logging
from fastapi.middleware.cors import CORSMiddleware
# from app.routes.user import router as user_router


app = FastAPI(
    title="Mini IMDB",
    description="This is a mini IMDB project which is written and developed by FastAPI."
)

# Logging
logging.basicConfig(filename='errors.log', level=logging.ERROR)


@app.on_event("startup")
async def startup_db():
    await create_all_tables()


# Middlewares
allowed_origins = [
    "http://localhost:3000",  # TODO get from db
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CustomMiddleware)


# # APIs
# app.include_router(user_router, prefix="/user", tags=["User"])
