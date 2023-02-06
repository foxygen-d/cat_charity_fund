from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_full_invested_objects(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(obj_in).where(obj_in.fully_invested == 0
                             ).order_by(obj_in.create_date)
    )
    return objects.scalars().all()


async def close_donation_for_obj(obj_in: Union[CharityProject, Donation]):
    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
    return obj_in


async def invest_money(
    obj_in: Union[CharityProject, Donation],
    obj_model: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:
    free_amount_in = obj_in.full_amount - obj_in.invested_amount
    free_amount_in_model = obj_model.full_amount - obj_model.invested_amount

    if free_amount_in > free_amount_in_model:
        obj_in.invested_amount += free_amount_in_model
        await close_donation_for_obj(obj_model)

    elif free_amount_in == free_amount_in_model:
        await close_donation_for_obj(obj_in)
        await close_donation_for_obj(obj_model)

    else:
        obj_model.invested_amount += free_amount_in
        await close_donation_for_obj(obj_in)

    return obj_in, obj_model


async def investing_process(
    obj_in: Union[CharityProject, Donation],
    model_add: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    objects_model = await get_not_full_invested_objects(model_add, session)

    for model in objects_model:
        obj_in, model = await invest_money(obj_in, model)
        session.add(obj_in)
        session.add(model)

    await session.commit()
    await session.refresh(obj_in)
    return obj_in
