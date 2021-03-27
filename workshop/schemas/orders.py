from pydantic import BaseModel, Field, Extra


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