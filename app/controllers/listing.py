from sqlalchemy.orm import Session, defer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Listing
from app.schemas import ICreateListingController, IUpdateListing
from app.utils.error_handler import ErrorHandler


class ListingController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        listings = (await self.db.execute(select(Listing).options(defer(Listing.ownerId)))).scalars().all()
        return listings

    async def get_by_owner_id(self, owner_id: int):
        listings = (await self.db.execute(select(Listing).where(Listing.ownerId == owner_id))).all()
        return listings

    async def get_by_id(self, id: int):
        listing = (await self.db.execute(select(Listing).where(Listing.id == id))).scalar_one_or_none()
        if not listing:
            raise ErrorHandler.not_found("Listing")
        return listing

    async def create(self, listing_items: ICreateListingController):
        async with self.db as async_session:
            new_listing = Listing(
                type=listing_items["type"],
                availableNow=listing_items["availableNow"],
                ownerId=listing_items["ownerId"],
                address=listing_items["address"]
            )
            async_session.add(new_listing)
            await async_session.commit()
            await async_session.refresh(new_listing)
            return new_listing

    async def update_by_id(self, id: int, listing_items: IUpdateListing):
        listing = await self.get_by_id(id=id)

        if listing:
            for key, value in listing_items.items():
                setattr(listing, key, value)
            await self.db.commit()
        return listing

    async def delete(self, id: int):
        listing = await self.get_by_id(id=id)
        if not listing:
            raise ErrorHandler.not_found("Listing")
        await self.db.delete(listing)
        await self.db.commit()
        return

    async def check_user_is_owner(self, user_id, listing_id):
        listing = await self.get_by_id(id=listing_id)

        if listing.ownerId != user_id:
            raise ErrorHandler.access_denied("Listing")
