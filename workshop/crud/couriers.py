from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import InstrumentedList
from datetime import datetime
from workshop import models
from workshop import schemas
from workshop.utils import utils
from workshop.crud import orders


def _get_courier(db: Session, courier_id: int) -> models.Courier:
    db_courier: models.Courier = db.query(models.Courier).filter(models.Courier.courier_id == courier_id).first()
    if db_courier is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='courier_id does not exist!')
    return db_courier


def create_courier(db: Session, courier: schemas.Courier):
    db_courier: models.Courier = db.query(models.Courier)\
        .filter(models.Courier.courier_id == courier.courier_id)\
        .first()
    if db_courier:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'courier_id = {courier.courier_id} already exist')
    db_courier = models.Courier(courier_id=courier.courier_id,
                                courier_type=courier.courier_type)
    db.add(db_courier)
    for i in courier.regions:
        db_region = models.CourierRegion(region=i, courier_id=courier.courier_id)
        db.add(db_region)
    for i in courier.working_hours:
        (begin_time, end_time) = i.split('-')
        begin_time = datetime.strptime(begin_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')
        db_hours = models.CourierWorkHour(begin_time=begin_time, end_time=end_time, courier_id=courier.courier_id)
        db.add(db_hours)
    db.commit()


def patch_courier(db: Session, uid: int, data: schemas.CourierPatch) -> models.Courier:
    db_courier: models.Courier = db.query(models.Courier).filter(models.Courier.courier_id == uid).first()
    db_courier = orders.remove_order_patch_update(db, db_courier)
    for field, value in data.dict(exclude_none=True).items():
        if field == 'regions':
            regions = [models.CourierRegion(region=i) for i in value]
            db_courier.regions = regions
            continue
        if field == 'working_hours':
            hours = [models.CourierWorkHour(**utils.str2datetime(s)) for s in value]
            db_courier.working_hours = hours
            continue
        setattr(db_courier, field, value)
    db.commit()
    db.refresh(db_courier)
    orders.orders_assign(db, db_courier.courier_id)
    return db_courier


def get_rating_courier(db: Session, courier_id: int) -> models.Courier:
    db_courier: models.Courier = _get_courier(db, courier_id)
    if db_courier.earnings == 0:
        rating = None
    else:
        average_time: list[float] = []
        for region in db_courier.regions:
            if region.number_completed_order != 0:
                average_time.append(region.sum_delivery_time/region.number_completed_order)
        t = min(average_time)
        rating = (60*60 - min(t, 60*60))/(60*60) * 5
    db_courier.rating = rating
    return db_courier
