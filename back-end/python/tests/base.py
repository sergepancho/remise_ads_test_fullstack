# -*- coding: utf-8 -*-
import unittest
import jwt
from datetime import datetime, timedelta
from app import create_app, db


class TestConfig:
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    JWT_SECRET_KEY = 'test-secret-key'
    JWT_EXPIRATION_HOURS = 24

    @staticmethod
    def init_app(app):
        pass


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_auth_token(self):
        response = self.client.post('/api/auth/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        return response.get_json()['token']

    def auth_header(self, token=None):
        if token is None:
            token = self.get_auth_token()
        return {'Authorization': f'Bearer {token}'}
