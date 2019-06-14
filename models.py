from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class GasStation(db.Model):
    __tablename__ = 'station'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    fuel_price = db.Column(db.Integer)
    cars = db.relationship('Car')

    def __init__(self, request, list_cars):
        self.name = request['name']
        if 'fuel_price' in request:
            self.fuel_price = request['fuel_price']
        self.cars = list_cars

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'fuel_price': self.fuel_price, 'cars': [car.to_dict() for car in self.cars]}

    def set_station(self, request, list_cars):
        if 'name' in request:
            self.name = request['name']
        if 'fuel_price' in request:
            self.fuel_price = request['fuel_price']
        self.cars = list_cars



class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'))

    def __init__(self, request):
        self.name = request['name']
        if 'description' in request:
            self.description = request['description']

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'station_id': self.station_id}

    def set_car(self, request):
        if 'name' in request:
            self.name = request['name']
        if 'description' in request:
            self.description = request['description']

    def set_station_id(self, station_id):
        self.station_id = station_id
