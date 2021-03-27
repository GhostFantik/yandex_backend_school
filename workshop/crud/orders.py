from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from datetime import datetime
from workshop.utils import enums
from workshop import models
from workshop import schemas


def create_order(db: Session, order: schemas.Order):
    db_order = models.Order(order_id=order.order_id,
                            weight=order.weight,
                            region=order.region)
    db.add(db_order)
    for i in order.delivery_hours:
        (begin_time, end_time) = i.split('-')
        begin_time = datetime.strptime(begin_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')
        db_hours = models.OrderDeliveryHour(begin_time=begin_time, end_time=end_time, order_id=order.order_id)
        db.add(db_hours)
    db.commit()


def orders_assign(db: Session, courier_id: int) -> Optional[tuple[list[int], datetime]]:
    db_courier: models.Courier = db.query(models.Courier).filter(models.Courier.courier_id == courier_id).first()
    if db_courier is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='courier_id does not exist!')
    orders = find_orders(db, db_courier)
    if not len(orders):
        if db_courier.assign_time:
            db_courier.assign_time = None  # QUESTION
            db.add(db_courier)
            db.commit()
        return None
    if not db_courier.assign_time:
        db_courier.assign_time = datetime.now()
    db_courier.orders.extend(orders)
    db.add(db_courier)
    db.commit()
    return [i.order_id for i in orders], db_courier.assign_time


def find_orders(db: Session, db_courier: models.Courier) -> list[models.Order]:
    regions = [i.region for i in db_courier.regions]
    max_weight = enums.CourierTypeByWeight[db_courier.courier_type.value].value
    order_region: list[models.Order] = db \
        .query(models.Order) \
        .filter(models.Order.completed.is_(False)) \
        .filter(or_(models.Order.courier_id.is_(None), models.Order.courier_id == db_courier.courier_id)) \
        .filter(models.Order.region.in_(regions)).all()
    order_region_hour: list[models.Order] = []
    for order in order_region:
        flag = False
        for order_hour in order.delivery_hours:
            for courier_hour in db_courier.working_hours:
                if order_hour.begin_time <= courier_hour.begin_time <= order_hour.end_time:
                    flag = True
                elif courier_hour.begin_time <= order_hour.begin_time <= courier_hour.end_time:
                    flag = True
        if flag:
            order_region_hour.append(order)
    order_region_hour_weight: list[models.Order] = list(filter(
        lambda x: x.weight <= max_weight, order_region_hour))
    order_region_hour_weight.sort(key=lambda x: x.weight)
    ready_orders: list[models.Order] = []
    courier_weight = 0
    for order in order_region_hour_weight:
        courier_weight += order.weight
        if courier_weight <= max_weight:
            ready_orders.append(order)
        else:
            break
    return ready_orders


def remove_order_patch_update(db: Session, db_courier: models.Courier) -> models.Courier:
    """Служебный метод для удаления заказов у курьера, чтобы назначить их заново. Сохраняет assign_time"""
    db_courier.orders = [i for i in db_courier.orders if i.completed]
    db.commit()
    db.refresh(db_courier)
    return db_courier
