from pydantic import BaseModel, Field, Extra
from typing import Optional
from workshop.utils import enums


class Courier(BaseModel):
    courier_id: int
    courier_type: enums.CourierType
    regions: list[int]
    working_hours: list[str] = Field(..., regex=r'^\d\d:\d\d-\d\d:\d\d$')

    class Config:
        orm_mode = True
        extra = Extra.forbid


class CourierPatch(BaseModel):
    courier_id: Optional[int] = None
    courier_type: Optional[enums.CourierType] = None
    regions: Optional[list[int]] = None
    working_hours: Optional[list[str]] = Field(None, regex=r'^\d\d:\d\d-\d\d:\d\d$')

    class Config:
        extra = Extra.forbid


class CourierRating(Courier):
    rating: Optional[float]
    earnings: int
