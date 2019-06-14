#!flask/bin/python
from flask import jsonify, abort, request
from models import app, db, Car, GasStation
import json


@app.route('/')
def index():
    return "Hello, World"


########################### GET ################################

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    list = [car.to_dict() for car in cars]
    return jsonify(list)

@app.route('/stations', methods=['GET'])
def get_stations():
    stations = GasStation.query.all()
    list = [station.to_dict() for station in stations]
    return jsonify(list)



@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    car = Car.query.get_or_404(car_id)
    return jsonify({'car': car.to_dict()})


@app.route('/stations/<int:station_id>', methods=['GET'])
def get_station(station_id):
    station = GasStation.query.get_or_404(station_id)
    return jsonify({'station': station.to_dict()})



########################### POST ################################

@app.route('/cars', methods=['POST'])
def create_car():
    req = request.json
    if not req:
        abort(400)
    car = Car(req)
    db.session.add(car)
    db.session.commit()
    return jsonify(car.to_dict()), 201


@app.route('/stations', methods=['POST'])
def create_station():
    req = request.json
    if not req:
        abort(400)
    existing_cars = Car.query.filter(Car.id.in_(req['cars'])).all() if 'cars' in req else []
    station = GasStation(req, existing_cars)
    for car in existing_cars:
        c = Car.query.get(car.id)
        c.set_station_id(station.id)
    db.session.add(station)
    db.session.commit()
    return jsonify(station.to_dict()), 201

########################### PUT ################################

@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    req = request.json
    if not req:
        abort(400)
    car = Car.query.get_of_404(car_id)
    car.set_car(req)
    db.session.commit()
    return jsonify({'car': car.to_dict()})


@app.route('/stations/<int:station_id>', methods=['PUT'])
def update_station(station_id):
    req = request.json
    if not req:
        abort(400)
    station = GasStation.query.get_or_404(station_id)
    existing_cars = Car.query.filter(Car.id.in_(req['cars'])).all() if 'cars' in req else []
    station.set_station(req, existing_cars)
    for car in existing_cars:
        c = Car.query.get(car.id)
        c.set_station_id(station.id)
    db.session.commit()
    return jsonify({'station': station.to_dict()})


########################### DELETE ################################

@app.route('/cars', methods=['DELETE'])
def delete_cars():
    cars = Car.query.all()
    for car in cars:
        db.session.delete(car)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/stations', methods=['DELETE'])
def delete_stations():
    stations = GasStation.query.all()
    for station in stations:
        db.session.delete(station)
    db.session.commit()
    return jsonify({'result': True})



@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/stations/<int:station_id>', methods=['DELETE'])
def delete_station(station_id):
    station = GasStation.query.get_or_404(station_id)
    db.session.delete(station)
    db.session.commit()
    return jsonify({'result': True})



if __name__ == '__main__':
    app.run(debug=True)
