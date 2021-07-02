from flask_apispec import MethodResource
from flask_apispec import doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from db.db import DB
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access


class GetArticleEnums(MethodResource, Resource):

    def __init__(self, db: DB):
        self.db = db

    @log_request
    @doc(tags=['article'],
         description='Get enumerations of article fields',
         responses={
             "200": {},
         })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def get(self):

        data = {
            "status": self.db.tables["Article"].status.prop.columns[0].type.enums,
            "type": self.db.tables["Article"].type.prop.columns[0].type.enums
        }

        return data, "200 "
