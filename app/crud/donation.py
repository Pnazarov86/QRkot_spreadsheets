from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate
from app.services.investment import investment


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self, session: AsyncSession, user: User
    ):
        """Получение пожертвований пользователя."""
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()

    async def create_donation(
        self,
        donation: DonationCreate,
        session: AsyncSession,
        user: User
    ):
        """Создание пожертвований (Для зарегистрированных пользователей)."""
        new_donation = await self.create(donation, session, user)
        await investment(session, new_donation)
        return new_donation


donation_crud = CRUDDonation(Donation)
