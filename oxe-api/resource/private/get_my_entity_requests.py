from flask_apispec import MethodResource
from flask_apispec import doc
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from db.db import DB
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from utils.serializer import Serializer


class GetMyEntityRequests(MethodResource, Resource):

    def __init__(self, db: DB):
        self.db = db

    @log_request
    @doc(tags=['private'],
         description='Get the list of requests of the specified entity',
         responses={
             "200": {},
             "422": {"description": "Object not found or you don't have the required access to it"},
         })
    @jwt_required
    @catch_exception
    def get(self, id_):

        try:
            self.db.session \
                .query(self.db.tables["UserEntityAssignment"]) \
                .with_entities(self.db.tables["UserEntityAssignment"].entity_id) \
                .filter(self.db.tables["UserEntityAssignment"].user_id == get_jwt_identity()) \
                .filter(self.db.tables["UserEntityAssignment"].entity_id == int(id_)) \
                .one()
        except NoResultFound:
            return "", "422 Object not found or you don't have the required access to it"

        data = Serializer.serialize(
            self.db.session
                .query(self.db.tables["UserRequest"])
                .filter(self.db.tables["UserRequest"].entity_id == int(id_))
                .all(),
            self.db.tables["UserRequest"]
        )

        return data, "200 "
