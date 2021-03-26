from pydantic import BaseModel, Field
from enum import Enum


class CourierType(Enum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'


class CourierIn(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: list[int] = None
    working_hours: list[str] = Field(..., regex=r'^\d\d:\d\d-\d\d:\d\d$')





