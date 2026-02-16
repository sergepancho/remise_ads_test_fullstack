# -*- coding: utf-8 -*-
from app import db
from app.models.entities import VehicleMake, VehicleModel, Vehicle
from tests.base import BaseTestCase


class TestVehicleEndpoints(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Insert test data
        make1 = VehicleMake(vehicle_make_id=1, name='Toyota', url='toyota', state=1)
        make2 = VehicleMake(vehicle_make_id=2, name='Honda', url='honda', state=0)  # inactive
        db.session.add_all([make1, make2])

        model1 = VehicleModel(vehicle_model_id=1, name='Camry', state=1)
        model2 = VehicleModel(vehicle_model_id=2, name='Corolla', state=1)
        model3 = VehicleModel(vehicle_model_id=3, name='Civic', state=1)
        db.session.add_all([model1, model2, model3])

        v1 = Vehicle(vehicle_make_id=1, vehicle_model_id=1, vehicle_year=2023, state=1)
        v2 = Vehicle(vehicle_make_id=1, vehicle_model_id=1, vehicle_year=2022, state=1)
        v3 = Vehicle(vehicle_make_id=1, vehicle_model_id=2, vehicle_year=2023, state=1)
        v4 = Vehicle(vehicle_make_id=1, vehicle_model_id=2, vehicle_year=2021, state=0)  # inactive
        db.session.add_all([v1, v2, v3, v4])

        db.session.commit()

    def test_get_vehicle_makes_returns_active_only(self):
        response = self.client.get('/api/vehicle-makes',
                                   headers=self.auth_header())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        makes = data['vehicle_makes']
        self.assertEqual(len(makes), 1)
        self.assertEqual(makes[0]['name'], 'Toyota')

    def test_get_vehicle_models_by_make(self):
        response = self.client.get('/api/vehicle-makes/1/models',
                                   headers=self.auth_header())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        models = data['vehicle_models']
        names = [m['name'] for m in models]
        self.assertIn('Camry', names)
        self.assertIn('Corolla', names)

    def test_get_vehicle_years(self):
        response = self.client.get('/api/vehicle-years',
                                   headers=self.auth_header())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        years = data['vehicle_years']
        self.assertIn(2023, years)
        self.assertIn(2022, years)
        # 2021 vehicle is inactive (state=0), should not appear
        self.assertNotIn(2021, years)

    def test_get_coverage_by_make(self):
        response = self.client.get('/api/vehicle-makes/1/coverage',
                                   headers=self.auth_header())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        coverage = data['coverage']
        self.assertIn('Camry', coverage)
        self.assertIn(2023, coverage['Camry'])
        self.assertIn(2022, coverage['Camry'])

    def test_get_models_empty_for_inactive_make(self):
        # make_id=2 (Honda) is inactive, no active vehicles linked
        response = self.client.get('/api/vehicle-makes/2/models',
                                   headers=self.auth_header())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['vehicle_models']), 0)

    def test_get_coverage_empty_for_make_without_active_vehicles(self):
        response = self.client.get('/api/vehicle-makes/2/coverage',
                                   headers=self.auth_header())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['coverage']), 0)
