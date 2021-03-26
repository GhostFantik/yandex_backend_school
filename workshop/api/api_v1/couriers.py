from fastapi import APIRouter
from app.schemas.couriers import CourierIn


router = APIRouter()


@router.post('/')
def create_couriers(data: CourierIn):
    print(data)


@router.patch('/{courier_id}')
def update_courier(courier_id: int):
    pass

