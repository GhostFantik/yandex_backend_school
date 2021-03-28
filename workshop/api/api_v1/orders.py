from typing import Optional
from fastapi import APIRouter, Body, Depends, status
from fastapi.exceptions import ValidationError, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from sqlalchemy.orm import Session
from workshop.db.database import get_db
from workshop.schemas import Order, OrderAssignIn, OrderCompleteIn
from workshop import crud


router = APIRouter()


@router.post('/assign')
def orders_assign(db: Session = Depends(get_db), data: dict = Body(...)):
    try:
        courier_id = OrderAssignIn.parse_obj(data).courier_id
    except ValidationError as e:
        content = jsonable_encoder({
            'validation_error': {
                'info': e.errors()
            }
        })
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=content)
    resp: Optional[tuple[list[int], datetime]] = crud.orders_assign(db, courier_id)
    if not resp:
        return []
    order_ids: list[int] = resp[0]
    assign_time: datetime = resp[1]
    content = jsonable_encoder({
        'orders': [{'id': i} for i in order_ids],
        'assign_time': assign_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    })
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.post('/complete')
def complete_order(db: Session = Depends(get_db), data: dict = Body(...)):
    try:
        data = OrderCompleteIn.parse_obj(data)
        db_order: Order = crud.complete_order(db, data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({'order_id': db_order.order_id}))
    except ValidationError as e:
        content = jsonable_encoder({
            'validation_error': {
                'info': e.errors()
            }
        })
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=content)


@router.post('/')
def create_orders(data: list[dict] = Body(..., embed=True), db: Session = Depends(get_db)):
    validated_data: list[Order] = []
    validated_data_id: list[dict[str, int]] = []
    invalidated_data_id: list[dict[str, any]] = []
    if not len(data):
        raise RequestValidationError
    for item in data:
        try:
            order: Order = Order.parse_obj(item)
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
        for i in validated_data:
            crud.create_order(db, i)
        content = jsonable_encoder({
            'orders': validated_data_id
        })
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=content)


