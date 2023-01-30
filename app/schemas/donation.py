from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, root_validator, validator, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    id: Optional[int]
    create_date: datetime

    @validator('create_date')
    def check_create_date_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError(
                'Время создания проекта '
                'не может быть меньше текущего времени'
            )
        return value

    @root_validator(skip_on_failure=True)
    def check_create_date_before_close_date(cls, values):
        if values['create_date'] >= values['close_date']:
            raise ValueError(
                'Время создания проекта '
                'не может быть больше времени окончания'
            )
        return values


class DonationDB(DonationCreate):
    id: Optional[int]
    create_date: datetime
    user_id: Optional[int]
    invested_amount: PositiveInt
    fully_invested: bool
    close_date: datetime

    class Config:
        orm_mode = True


class DonationUpdate(DonationBase):
    pass
