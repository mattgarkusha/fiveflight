from flask import Flask, jsonify, request
from adapters import orm
from api import views
from domain.commands import *
import bootstrap

app = Flask(__name__)
message_bus = bootstrap.bootstrap()

@app.before_first_request
def create_tables():
    orm.create_tables()

@app.route('/api/aircraft', methods=['GET'])
def list_aircraft():
    result = views.get_aircraft(message_bus.uow)
    if not result:
        return []
    return jsonify(result), 200

@app.route('/api/aircraft', methods=['POST'])
def create_aircraft():
    data = request.json
    cmd = AddAircraftCommand(data['name'], data['make'], data['model'], data['tail_number'])
    aircraft = message_bus.handle(message=cmd)
    return jsonify(aircraft)

@app.route('/api/aircraft/<int:id>', methods=['GET'])
def get_aircraft(id):
    result = views.get_aircraft_by_id(id, message_bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200

@app.route('/api/aircraft/<int:id>', methods=['PUT'])
def update_aircraft(id):
    data = request.json
    cmd = EditAircraftCommand(
        id=id,
        name=data.get('name'),
        make=data.get('make'),
        model=data.get('model'),
        tail_number=data.get('tail_number')
    )
    aircraft = message_bus.handle(message=cmd)
    if aircraft is None:
        return jsonify({'error': 'Aircraft not found'}), 404
    return jsonify(aircraft)

@app.route('/api/aircraft/<int:id>', methods=['DELETE'])
def delete_aircraft(id):
    cmd = DeleteAircraftCommand(id=id)
    aircraft = message_bus.handle(message=cmd)
    if aircraft is None:
        return jsonify({'error': 'Aircraft not found'}), 404
    return jsonify(aircraft)

@app.route('/api/flightplan', methods=['GET'])
def list_flight_plans():
    result = views.get_flight_plans(message_bus.uow)
    if not result:
        return []
    return jsonify(result), 200

@app.route('/api/flightplan/by_aircraft_id/<int:aircraft_id>', methods=['GET'])
def get_flight_plans_by_aircraft_id(aircraft_id):
    result = views.get_flight_plans_by_aircraft_id(aircraft_id, message_bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200

@app.route('/api/flightplan/by_tail_number/<string:tail_number>', methods=['GET'])
def get_flight_plans_by_tail_number(tail_number):
    result = views.get_flight_plans_by_tail_number(tail_number, message_bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200

@app.route('/api/flightplan', methods=['POST'])
def create_flight_plan():
    data = request.json
    cmd = AddFlightPlanCommand(
        aircraft_id=data['aircraft_id'],
        origin=data['origin'],
        destination=data['destination'],
        departure_time=data['departure_time'],
        arrival_time=data['arrival_time']
    )
    flight_plan = message_bus.handle(message=cmd)
    return jsonify(flight_plan)

@app.route('/api/flightplan/<int:id>', methods=['PUT'])
def update_flight_plan(id):
    data = request.json
    cmd = EditFlightPlanCommand(
        id=id,
        aircraft_id=data.get('aircraft_id'),
        origin=data.get('origin'),
        destination=data.get('destination'),
        departure_time=data.get('departure_time'),
        arrival_time=data.get('arrival_time')
    )
    flight_plan = message_bus.handle(message=cmd)
    if flight_plan is None:
        return jsonify({'error': 'Flight plan not found'}), 404
    return jsonify(flight_plan)

@app.route('/api/flightplan/<int:id>', methods=['DELETE'])
def delete_flight_plan(id):
    cmd = DeleteFlightPlanCommand(id=id)
    flight_plan = message_bus.handle(message=cmd)
    if flight_plan is None:
        return jsonify({'error': 'Flight plan not found'}), 404
    return jsonify(flight_plan)
