from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.utils.error_handler import ErrorHandler
from app.controllers.listing import ListingController
from app.controllers.user import UserController
from app.schemas import ICreateListingBody, IUpdateListing
from app.dependencies.authentication import get_token_info

router = APIRouter()


# get all
@router.get("/all")
async def get_all_route(
    token_info: str = Depends(get_token_info),
    db: AsyncSession = Depends(get_db)
):
    scope = token_info["scope"]
    user_controller = UserController(db)

    # check scope
    user_controller.validate_scope(scope=scope, operation="get_all_listings")

    listing_controller = ListingController(db)
    listings = await listing_controller.get_all()
    await db.close()
    return listings


# get by id
@router.get("/{id}")
async def get_by_id_route(
        token_info: str = Depends(get_token_info),
        id: int = Path(description="ID of listing to retrieve"),
        db: AsyncSession = Depends(get_db)
):
    current_user = token_info["user"]
    scope = token_info["scope"]
    user_controller = UserController(db)

    # check scope
    user_controller.validate_scope(scope=scope, operation="get_listing")

    listing_controller = ListingController(db)
    listing = await listing_controller.get_by_id(id)
    await db.close()

    if current_user.id != listing.ownerId:
        if hasattr(listing, "ownerId"):
            delattr(listing, "ownerId")

    return listing


# create
@router.post("/")
async def create_route(
        data: ICreateListingBody,
        token_info: str = Depends(get_token_info),
        db: AsyncSession = Depends(get_db)
):
    current_user = token_info["user"]
    scope = token_info["scope"]
    user_controller = UserController(db)

    # check scope
    user_controller.validate_scope(scope=scope, operation="create_listing")

    listing_controller = ListingController(db)

    # create a new listing
    listing_items = {
        "type": data.type,
        "availableNow": data.availableNow,
        "ownerId": current_user.id,
        "address": data.address
    }
    listing = await listing_controller.create(listing_items=listing_items)
    await db.close()

    return listing


# update by id
@router.put("/{id}")
async def update_route(
        data: IUpdateListing,
        token_info: str = Depends(get_token_info),
        id: int = Path(description="This is ID of user to update"),
        db: AsyncSession = Depends(get_db)
):
    current_user = token_info["user"]
    scope = token_info["scope"]
    user_controller = UserController(db)

    # check scope
    user_controller.validate_scope(scope=scope, operation="update_listing")

    listing_controller = ListingController(db)

    # check owner_id
    await listing_controller.check_user_is_owner(
        user_id=current_user.id, listing_id=id)

    # update listing
    listing_items = {
        "type": data.type,
        "availableNow": data.availableNow,
        "address": data.address
    }
    await listing_controller.update_by_id(id, listing_items=listing_items)
    await db.close()

    return {"message": "Listing updated successfully"}


# delete by id
@router.delete("/{id}")
async def delete_route(
        token_info: str = Depends(get_token_info),
        id: int = Path(description="ID of listing to delete"),
        db: AsyncSession = Depends(get_db)
):
    current_user = token_info["user"]
    scope = token_info["scope"]
    user_controller = UserController(db)

    # check scope
    user_controller.validate_scope(scope=scope, operation="delete_listing")

    listing_controller = ListingController(db)

    # check owner_id
    await listing_controller.check_user_is_owner(
        user_id=current_user.id, listing_id=id)

    # delete listing
    await listing_controller.delete(id)
    await db.close()

    return {"message": "Listing deleted successfully"}
