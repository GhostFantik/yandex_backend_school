from sqlalchemy import Column, Integer, Float, Enum, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from workshop.db.database import Base


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    weight = Column(Float, index=True)
    region = Column(Integer, index=True)
    completed = Column(Boolean, default=False)
    courier_id = Column(Integer, ForeignKey('couriers.courier_id'), index=True)

    delivery_hours = relationship('OrderDeliveryHour', back_populates='order')
    courier = relationship('Courier', back_populates='orders')

    def __str__(self):
        return self.order_id


class OrderDeliveryHour(Base):
    __tablename__ = 'orders_hours'
    id = Column(Integer, primary_key=True)
    begin_time = Column(DateTime, index=True)
    end_time = Column(DateTime, index=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), index=True)

    order = relationship('Order', back_populates='delivery_hours')
