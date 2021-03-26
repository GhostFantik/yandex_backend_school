from pydantic import BaseModel, Field


class OrderIn(BaseModel):
    order_id: int
    weight: float
    region: int
    delivery_hours: list[str] = Field(..., regex=r'^\d\d:\d\d-\d\d:\d\d$')

