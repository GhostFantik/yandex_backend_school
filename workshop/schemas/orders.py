from pydantic import BaseModel, Field, Extra
from datetime import datetime


class Order(BaseModel):
    order_id: int
    weight: float
    region: int
    delivery_hours: list[str] = Field(..., regex=r'^\d\d:\d\d-\d\d:\d\d$')

    class Config:
        extra = Extra.forbid


class OrderAssignIn(BaseModel):
    courier_id: int

    class Config:
        extra = Extra.forbid


class OrderCompleteIn(BaseModel):
    courier_id: int
    order_id: int
    complete_time: datetime

    class Config:
        extra = Extra.forbid
