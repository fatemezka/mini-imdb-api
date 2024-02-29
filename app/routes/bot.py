from fastapi import APIRouter
from app.utils.weatherapi_receiver import main

router = APIRouter()


@router.get("/")
async def create_time_route():
    main()
    return {"message": "Next 10 days weather info saved in 'time.csv' file."}
