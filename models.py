from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_appbuilder import Model


class GasStation(Model):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    fuel_price = Column(Integer)
    car_observers = relationship("Car", backref="station")

    def __init__(self, id, request):
        self.id = id
        self.name = request['name']
        if 'fuel_price' in request:
            self.fuel_price = request['fuel_price']
        if 'car_observers' in request:
            self.car_observers = request['car_observers']

    def station_to_dict(self):
        return {'id': self.id, 'name': self.name, 'fuel_price': self.fuel_price, 'car_observers': self.car_observers}

    def set_station(self, request):
        if 'name' in request:
            self.name = request['name']
        if 'fuel_price' in request:
            self.fuel_price = request['fuel_price']
        if 'car_observers' in request:
            self.car_observers = request['car_observers']

    def get_id(self):
        return self.id


class Car(Model):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100))
    station_id = Column(Integer, ForeignKey('station.id'))

    def __init__(self, id, request):
        self.id = id
        self.name = request['name']
        if 'description' in request:
            self.description = request['description']
        if 'station_id' in request:
            self.station_id = request['station_id']

    def car_to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'station_id': self.station_id}

    def set_car(self, request):
        if 'name' in request:
            self.name = request['name']
        if 'description' in request:
            self.description = request['description']
        if 'station_id' in request:
            self.station_id = request['station_id']

    def get_id(self):
        return self.id
