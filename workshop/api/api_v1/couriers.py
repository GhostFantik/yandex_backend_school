from fastapi import APIRouter, Body, Depends, status
from fastapi.exceptions import ValidationError, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from workshop.db.database import get_db
from workshop.schemas.couriers import Courier, CourierPatch, CourierRating
from workshop import crud
from workshop.utils import utils


router = APIRouter()


@router.post('')
def create_couriers(data: list[dict] = Body(..., embed=True), db: Session = Depends(get_db)):
    validated_data: list[Courier] = []
    validated_data_id: list[dict[str, int]] = []
    invalidated_data_id: list[dict[str, int]] = []
    if not len(data):
        raise RequestValidationError
    for item in data:
        try:
            courier: Courier = Courier.parse_obj(item)
            validated_data.append(courier)
            validated_data_id.append({'id': courier.courier_id})
        except ValidationError as e:
            courier_id = item.get('courier_id')
            if courier_id is not None:
                invalidated_data_id.append({'id': courier_id, 'info': e.errors()})
    if len(invalidated_data_id):
        content = jsonable_encoder({
            'validation_error': {
                'couriers': invalidated_data_id
            }
        })
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=content)
    else:
        for i in validated_data:
            crud.create_courier(db, i)
        content = jsonable_encoder({
            'couriers': validated_data_id
        })
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=content)


@router.patch('/{courier_id}', response_model=Courier)
def update_courier(courier_id: int, data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        updated_data: CourierPatch = CourierPatch.parse_obj(data)
        db_courier = crud.patch_courier(db, courier_id, updated_data)
        courier = Courier(
            courier_id=db_courier.courier_id,
            courier_type=db_courier.courier_type,
            regions=[i.region for i in db_courier.regions],
            working_hours=[utils.datetime2str(i.begin_time, i.end_time) for i in db_courier.working_hours]
        )
        return courier
    except ValidationError as e:
        content = jsonable_encoder({
            'validation_error': {
                'info': e.errors()
            }
        })
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=content)


@router.get('/{courier_id}', response_model=CourierRating)
def get_courier(courier_id: int, db:Session = Depends(get_db)):
    db_courier = crud.get_rating_courier(db, courier_id)
    courier = CourierRating(
        courier_id=db_courier.courier_id,
        courier_type=db_courier.courier_type,
        regions=[i.region for i in db_courier.regions],
        working_hours=[utils.datetime2str(i.begin_time, i.end_time) for i in db_courier.working_hours],
        rating=db_courier.rating,
        earnings=db_courier.earnings
    )
    return courier
