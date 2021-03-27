from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import InstrumentedList
from datetime import datetime
from workshop import models
from workshop import schemas
from workshop.utils import utils
from workshop.crud import orders


def create_courier(db: Session, courier: schemas.Courier):
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



