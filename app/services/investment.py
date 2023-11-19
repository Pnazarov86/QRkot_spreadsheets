from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investment(
    session: AsyncSession,
    obj: Union[CharityProject, Donation]
):
    target = CharityProject if isinstance(obj, Donation) else Donation

    invest_models = await session.execute(
        select(target).where(
            target.fully_invested.is_(False)
        ).order_by('create_date')
    )

    for model in invest_models.scalars().all():
        amount_to_donate = min(
            model.full_amount - model.invested_amount,
            obj.full_amount - obj.invested_amount
        )
        model.invested_amount += amount_to_donate
        obj.invested_amount += amount_to_donate

        if model.invested_amount == model.full_amount:
            model.fully_invested = True
            model.close_date = datetime.now()

        if obj.invested_amount == obj.full_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()

    await session.commit()
    await session.refresh(obj)
    return obj
