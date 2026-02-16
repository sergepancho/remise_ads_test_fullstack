# -*- coding: utf-8 -*-
"""
    app.api.vehicle
    ~~~~~~~~~~~~~~

    Endpoint for the vehicle

    :copyright: (c) 2023 by Automotive Data Solution.
"""

from . import api
from .auth import token_required
from flask import jsonify, request
from app.services.vehicle import VehicleService


@api.route('/vehicle-makes', methods=['GET'])
@token_required
def vehicle_make_list():
    lst_vehicle_make = VehicleService.find_all_vehicle_make()
    return jsonify(vehicle_makes=lst_vehicle_make)


@api.route('/vehicle-makes/<int:make_id>/models', methods=['GET'])
@token_required
def vehicle_model_list(make_id):
    models = VehicleService.find_models_by_make(make_id)
    return jsonify(vehicle_models=models)


@api.route('/vehicle-years', methods=['GET'])
@token_required
def vehicle_year_list():
    years = VehicleService.find_all_years()
    return jsonify(vehicle_years=years)


@api.route('/vehicle-makes/<int:make_id>/coverage', methods=['GET'])
@token_required
def vehicle_coverage(make_id):
    coverage = VehicleService.find_coverage_by_make(make_id)
    return jsonify(coverage=coverage)


@api.route('/vehicle-makes/<int:make_id>/coverage/toggle', methods=['POST'])
@token_required
def toggle_coverage(make_id):
    data = request.get_json()
    model_id = data.get('vehicle_model_id')
    year = data.get('vehicle_year')
    new_state = VehicleService.toggle_vehicle_coverage(make_id, model_id, year)
    return jsonify(state=new_state)
