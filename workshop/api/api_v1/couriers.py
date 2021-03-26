from fastapi import APIRouter, Body, status
from fastapi.exceptions import ValidationError, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from workshop.schemas.couriers import CourierIn


router = APIRouter()


@router.post('/')
def create_couriers(data: list[dict] = Body(..., embed=True)):
    validated_data: list[CourierIn] = []
    validated_data_id: list[dict[str, int]] = []
    invalidated_data_id: list[dict[str, int]] = []
    if not len(data):
        raise RequestValidationError
    for item in data:
        try:
            courier: CourierIn = CourierIn.parse_obj(item)
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
        content = jsonable_encoder({
            'couriers': validated_data_id
        })
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=content)



@router.patch('/{courier_id}')
def update_courier(courier_id: int):
    pass

