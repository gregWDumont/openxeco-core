from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from decorator.verify_payload import verify_payload
from decorator.verify_admin_access import verify_admin_access
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request


class UpdateAddress(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    @log_request
    @catch_exception
    @verify_payload([
        {'field': 'id', 'type': int},
        {'field': 'address_1', 'type': str, 'optional': True},
        {'field': 'address_2', 'type': str, 'nullable': True, 'optional': True},
        {'field': 'number', 'type': str, 'nullable': True, 'optional': True},
        {'field': 'postal_code', 'type': str, 'nullable': True, 'optional': True},
        {'field': 'city', 'type': str, 'optional': True},
        {'field': 'administrative_area', 'type': str, 'nullable': True, 'optional': True},
        {'field': 'country', 'type': str, 'optional': True},
        {'field': 'latitude', 'type': [int, float], 'nullable': True, 'optional': True},
        {'field': 'longitude', 'type': [int, float], 'nullable': True, 'optional': True},
    ])
    @jwt_required
    @verify_admin_access
    def post(self):
        input_data = request.get_json()

        self.db.merge(input_data, self.db.tables["Company_Address"])

        return "", "200 "
