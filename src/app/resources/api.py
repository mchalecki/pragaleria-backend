import json

from flask import Blueprint, make_response
from flask_restful import Api

from app.resources.api_endpoints.auctions import Auctions
from app.resources.api_endpoints.catalog import Catalog
from app.resources.api_endpoints.exhibitions import Exhibitions
from app.resources.api_endpoints.terms_list import TermsList
from app.resources.api_endpoints.term_details import TermDetails

api_bl = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bl)


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(
        json.dumps(
            data,
            ensure_ascii=False
        ).encode('utf8'), code)
    resp.headers.extend(headers or {})
    return resp


def trail_slash(name):
    return '/' + name, '/' + name + '/'


api.add_resource(TermsList, *trail_slash('authors'))
api.add_resource(TermDetails, *trail_slash('authors/<int:term_id>'))
api.add_resource(Auctions, *trail_slash('auctions'))
api.add_resource(Exhibitions, *trail_slash('exhibitions'))
api.add_resource(Catalog, *trail_slash('catalog/<string:auction_id>'))
