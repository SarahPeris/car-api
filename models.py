from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask.appbuilder import Model

class GasStation(Model):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    fuel_price = Column(Integer)
    car_observers = relationship("Car", backref="station")

    def __repr__(self):
        return self.name


class Car(Model):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(string(100))
    station_id = Column(Integer, ForeignKey('station.id'))

    def __repr__(self):
        return self.name
