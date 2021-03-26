from fastapi import APIRouter
from workshop.api.api_v1 import couriers, orders


api_router = APIRouter()
api_router.include_router(couriers.router, prefix='/couriers', tags=['couriers'])
api_router.include_router(orders.router, prefix='/orders', tags=['orders'])
