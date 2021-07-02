from flask import request
from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs import fields

from db.db import DB
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access
from utils.serializer import Serializer


class GetArticles(MethodResource, Resource):

    def __init__(self, db: DB):
        self.db = db

    @log_request
    @doc(tags=['article'],
         description='Get articles',
         responses={
             "200": {},
         })
    @use_kwargs({
        'title': fields.Str(required=False),
        'type': fields.DelimitedList(fields.Str(), required=False),
        'taxonomy_values': fields.DelimitedList(fields.Str(), required=False),
    }, location="query")
    @jwt_required
    @verify_admin_access
    @catch_exception
    def get(self):

        filters = request.args.to_dict()
        article_objects = self.db.get_filtered_article_query(filters).all()
        data = Serializer.serialize(article_objects, self.db.tables["Article"])

        return data, "200 "
