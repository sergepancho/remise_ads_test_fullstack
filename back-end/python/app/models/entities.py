# -*- coding: utf-8 -*-
"""
    app.models.entities
    ~~~~~~~~~~~~~~

    All the entity of the database

    :copyright: (c) 2023 by Automotive Data Solution.
"""

from app import db


class VehicleMake(db.Model):
    __tablename__ = 'vehicle_make'
    __table_args__ = {'extend_existing': True}

    vehicle_make_id = db.Column('vehicle_make_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(255), nullable=False)
    url = db.Column('url', db.String(255), nullable=False)
    state = db.Column('state', db.Integer, default=1)
    updated = db.Column('updated', db.DateTime)


class VehicleModel(db.Model):
    __tablename__ = 'vehicle_model'
    __table_args__ = {'extend_existing': True}

    vehicle_model_id = db.Column('vehicle_model_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(255), nullable=False)
    state = db.Column('state', db.Integer, default=1)
    updated = db.Column('updated', db.DateTime)


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    __table_args__ = {'extend_existing': True}

    vehicle_id = db.Column('vehicle_id', db.Integer, primary_key=True, autoincrement=True)
    vehicle_make_id = db.Column('vehicle_make_id', db.Integer, db.ForeignKey('vehicle_make.vehicle_make_id'), nullable=False)
    vehicle_model_id = db.Column('vehicle_model_id', db.Integer, db.ForeignKey('vehicle_model.vehicle_model_id'), nullable=False)
    vehicle_year = db.Column('vehicle_year', db.SmallInteger)
    state = db.Column('state', db.Integer, default=1)
    updated = db.Column('updated', db.DateTime)
