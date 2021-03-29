from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from workshop.db.database import Base
from workshop.utils import enums


class Courier(Base):
    __tablename__ = 'couriers'
    courier_id = Column(Integer, primary_key=True, index=True)
    courier_type = Column(Enum(enums.CourierType))
    earnings = Column(Integer, default=0)
    assign_time = Column(DateTime, nullable=True, default=None)
    previous_time = Column(DateTime, nullable=True, default=None)
    rating = None

    regions = relationship('CourierRegion', back_populates='courier', cascade='all,delete')
    working_hours = relationship('CourierWorkHour', back_populates='courier')
    orders = relationship('Order', back_populates='courier')


class CourierRegion(Base):
    __tablename__ = 'couriers_regions'
    id = Column(Integer, primary_key=True)
    region = Column(Integer, index=True)
    number_completed_order = Column(Integer, default=0)
    sum_delivery_time = Column(Float, default=0)
    courier_id = Column(Integer, ForeignKey('couriers.courier_id', ondelete='CASCADE'), index=True)

    courier = relationship('Courier', back_populates='regions', cascade='all,delete')


class CourierWorkHour(Base):
    __tablename__ = 'couriers_hours'
    id = Column(Integer, primary_key=True)
    begin_time = Column(DateTime, index=True)
    end_time = Column(DateTime, index=True)
    courier_id = Column(Integer, ForeignKey('couriers.courier_id'), index=True)

    courier = relationship('Courier', back_populates='working_hours')

