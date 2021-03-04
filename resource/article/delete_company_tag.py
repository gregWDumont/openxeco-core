from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from decorator.verify_payload import verify_payload
from decorator.verify_admin_access import verify_admin_access
from decorator.catch_exception import catch_exception
from exception.object_not_found import ObjectNotFound
from decorator.log_request import log_request


class DeleteCompanyTag(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    @log_request
    @catch_exception
    @verify_payload([
        {'field': 'article', 'type': int},
        {'field': 'company', 'type': int}
    ])
    @jwt_required
    @verify_admin_access
    def post(self):
        input_data = request.get_json()

        row = {
            "article": input_data["article"],
            "company": input_data["company"]
        }

        companies = self.db.get(self.db.tables["ArticleCompanyTag"], row)

        if len(companies) > 0:
            self.db.delete(self.db.tables["ArticleCompanyTag"], row)
        else:
            raise ObjectNotFound

        return "", "200 "
