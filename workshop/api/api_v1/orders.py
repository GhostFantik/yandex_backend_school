from fastapi import APIRouter, Body, status
from fastapi.exceptions import ValidationError, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from workshop.schemas.orders import OrderIn


router = APIRouter()


@router.post('/')
def create_orders(data: list[dict] = Body(..., embed=True)):
    validated_data: list[OrderIn] = []
    validated_data_id: list[dict[str, int]] = []
    invalidated_data_id: list[dict[str, any]] = []
    if not len(data):
        raise RequestValidationError
    for item in data:
        try:
            order: OrderIn = OrderIn.parse_obj(item)
            validated_data.append(order)
            validated_data_id.append({'id': order.order_id})
        except ValidationError as e:
            order_id = item.get('order_id')
            if order_id is not None:
                invalidated_data_id.append({'id': order_id, 'info': e.errors()})
    if len(invalidated_data_id):
        content = jsonable_encoder({
            'validation_error': {
                'orders': invalidated_data_id
            }
        })
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=content)
    else:
        content = jsonable_encoder({
            'orders': validated_data_id
        })
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=content)
