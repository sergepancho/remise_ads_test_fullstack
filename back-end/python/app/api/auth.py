# -*- coding: utf-8 -*-
"""
    app.api.auth
    ~~~~~~~~~~~~~~

    Authentication endpoint and JWT decorator

    :copyright: (c) 2023 by Automotive Data Solution.
"""

import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from . import api

# Demo credentials (in production, these would come from a database)
DEMO_USER = 'admin'
DEMO_PASSWORD = 'admin123'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify(message='Token is missing'), 401

        try:
            jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify(message='Token has expired'), 401
        except jwt.InvalidTokenError:
            return jsonify(message='Token is invalid'), 401

        return f(*args, **kwargs)
    return decorated


@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify(message='Missing credentials'), 400

    username = data.get('username')
    password = data.get('password')

    if username == DEMO_USER and password == DEMO_PASSWORD:
        token = jwt.encode(
            {
                'user': username,
                'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS'])
            },
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify(token=token)

    return jsonify(message='Invalid credentials'), 401
