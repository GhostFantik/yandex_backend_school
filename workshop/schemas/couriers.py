from pydantic import BaseModel
from enum import Enum


class CourierType(Enum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'


class CourierIn(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: list[int]
    working_hours: list[str]

