# -*- coding: utf-8 -*-
"""
    app.services.vehicle
    ~~~~~~~~~~~~~~

    Service for the vehicle

    :copyright: (c) 2023 by Automotive Data Solution.
"""

from app.repositories.vehicle import VehicleMakeMapper, VehicleModelMapper, VehicleMapper


class VehicleService:

    @staticmethod
    def find_all_vehicle_make():
        mapper = VehicleMakeMapper()
        makes = mapper.find_all()
        return [dict(id=m.vehicle_make_id, name=m.name, url=m.url) for m in makes]

    @staticmethod
    def find_models_by_make(vehicle_make_id):
        mapper = VehicleModelMapper()
        models = mapper.find_by_make(vehicle_make_id)
        return [dict(id=m.vehicle_model_id, name=m.name) for m in models]

    @staticmethod
    def find_all_years():
        mapper = VehicleMapper()
        return mapper.find_distinct_years()

    @staticmethod
    def find_coverage_by_make(vehicle_make_id):
        mapper = VehicleMapper()
        return mapper.find_coverage_by_make(vehicle_make_id)

    @staticmethod
    def toggle_vehicle_coverage(vehicle_make_id, vehicle_model_id, vehicle_year):
        mapper = VehicleMapper()
        return mapper.toggle_vehicle(vehicle_make_id, vehicle_model_id, vehicle_year)
