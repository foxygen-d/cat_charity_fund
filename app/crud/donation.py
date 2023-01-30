from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import AsyncSessionLocal
from crud.base import CRUDBase
from models import Donation, User
from schemas.donation import DonationCreate


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self,  user: User, session: AsyncSession,
    ) -> List[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
