from fastapi import FastAPI
from app.database import create_all_tables
from app.middleware import CustomMiddleware
from app.utils.count_operator import increase_counter
from app.utils.fake_users_initializer import initialize_fake_users
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user import router as user_router
from app.routes.listing import router as listing_router
from app.routes.bot import router as bot_router


app = FastAPI(
    title="Dornica Fastapi Task",
    description="This is a Dornica tastapi task sample description"
)

# Logging
logging.basicConfig(filename='errors.log', level=logging.ERROR)


@app.on_event("startup")
async def startup_db():
    await create_all_tables()
    increase_counter()
    await initialize_fake_users()


# Middlewares
allowed_origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CustomMiddleware)


# Routes
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(listing_router, prefix="/listing", tags=["Listing"])
app.include_router(bot_router, prefix="/bot", tags=["Bot"])
