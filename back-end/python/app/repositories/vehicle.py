# -*- coding: utf-8 -*-
"""
    app.repositories.vehicle
    ~~~~~~~~~~~~~~

    Repository related to vehicles

    :copyright: (c) 2023 by Automotive Data Solution.
"""
from datetime import datetime
from app import db
from app.models.entities import VehicleMake, VehicleModel, Vehicle


class VehicleMakeMapper:

    def find_all(self):
        objs = VehicleMake.query.filter(VehicleMake.state == 1).all()
        return objs


class VehicleModelMapper:

    def find_by_make(self, vehicle_make_id):
        models = db.session.query(VehicleModel).join(
            Vehicle, Vehicle.vehicle_model_id == VehicleModel.vehicle_model_id
        ).filter(
            Vehicle.vehicle_make_id == vehicle_make_id,
            Vehicle.state == 1,
            VehicleModel.state == 1
        ).distinct().order_by(VehicleModel.name).all()
        return models


class VehicleMapper:

    def find_distinct_years(self):
        results = db.session.query(Vehicle.vehicle_year).filter(
            Vehicle.state == 1
        ).distinct().order_by(Vehicle.vehicle_year.desc()).all()
        return [r[0] for r in results]

    def find_coverage_by_make(self, vehicle_make_id):
        results = db.session.query(
            VehicleModel.name,
            VehicleModel.vehicle_model_id,
            Vehicle.vehicle_year
        ).join(
            VehicleModel, Vehicle.vehicle_model_id == VehicleModel.vehicle_model_id
        ).filter(
            Vehicle.vehicle_make_id == vehicle_make_id,
            Vehicle.state == 1
        ).order_by(VehicleModel.name, Vehicle.vehicle_year.desc()).all()

        coverage = {}
        for model_name, model_id, year in results:
            if model_name not in coverage:
                coverage[model_name] = []
            coverage[model_name].append(year)
        return coverage

    def toggle_vehicle(self, vehicle_make_id, vehicle_model_id, vehicle_year):
        vehicle = Vehicle.query.filter_by(
            vehicle_make_id=vehicle_make_id,
            vehicle_model_id=vehicle_model_id,
            vehicle_year=vehicle_year
        ).first()

        if vehicle:
            vehicle.state = 0 if vehicle.state == 1 else 1
            vehicle.updated = datetime.now()
            db.session.commit()
            return vehicle.state
        else:
            vehicle = Vehicle(
                vehicle_make_id=vehicle_make_id,
                vehicle_model_id=vehicle_model_id,
                vehicle_year=vehicle_year,
                state=1,
                updated=datetime.now()
            )
            db.session.add(vehicle)
            db.session.commit()
            return 1
