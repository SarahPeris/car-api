#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from models import Car, GasStation
import json
app = Flask(__name__)

@app.route('/')

def index():
    return "Hello, World"

cars = []
id_car = 0

stations = []
id_station = 0

########################### GET ################################

@app.route('/cars', methods=['GET'])
def get_cars():
    return jsonify(cars)

@app.route('/stations', methods=['GET'])
def get_stations():
    return jsonify({'stations': stations})



@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    for car in cars:
        if car.get_id() == car_id:
            return jsonify({'car': car.car_to_dict()})
    abort(404)

@app.route('/stations/<int:station_id>', methods=['GET'])
def get_station(station_id):
    for station in stations:
        if station.get_id() == station_id:
            return jsonify({'station': station.station_to_dict()})
    abort(404)



########################### POST ################################

@app.route('/cars', methods=['POST'])
def create_car():
    global id_car
    req = request.json
    if not req:
        abort(400)
    id_car += 1
    car = Car(id_car, req)
    cars.append(car)
    return jsonify({'car': car.car_to_dict()}), 201


@app.route('/stations', methods=['POST'])
def create_station():
    global id_station
    req = request.json
    if not req:
        abort(400)
    id_station += 1
    station = GasStation(id_station, req)
    stations.append(station)
    return jsonify({'station': station.station_to_dict()}), 201

########################### PUT ################################

@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    req = request.json
    if not req:
        abort(400)
    for car in cars:
        if car.get_id() == car_id:
            car.set_car(req)
            return jsonify({'car': car.car_to_dict()})
    abort(404)


@app.route('/stations/<int:station_id>', methods=['PUT'])
def update_station(station_id):
    req = request.json
    if not req:
        abort(400)
    for station in stations:
        if station.get_id() == station_id:
            station.set_station(req)
            return jsonify({'station': station.station_to_dict()})
    abort(404)


########################### DELETE ################################

@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    for car in cars:
        if car.get_id() == car_id:
            cars.remove(car)
    return jsonify({'result': True})

@app.route('/stations/<int:station_id>', methods=['DELETE'])
def delete_station(station_id):
    for station in stations:
        if station.get_id() == station_id:
            stations.remove(station)
    return jsonify({'result': True})




if __name__ == '__main__':
    app.run(debug=True)
