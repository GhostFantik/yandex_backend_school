from enum import Enum


class CourierType(Enum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'


class CourierTypeByWeight(Enum):
    foot = 10
    bike = 15
    car = 50


class CourierTypeByC(Enum):
    foot = 2
    bike = 5
    car = 9
