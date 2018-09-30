import json

from flask import Blueprint, make_response
from flask_restful import Api

from app.resources.api_endpoints.auctions import Auctions
from app.resources.api_endpoints.catalog import Catalog
from app.resources.api_endpoints.exhibitions import Exhibitions
from app.resources.api_endpoints.terms import TermsList, TermDetails

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


api.add_resource(TermsList,
    '/authors',
    '/authors/',
    '/authors/<int:page_number>/<int:page_size>'
)
api.add_resource(TermDetails,
    '/authors/details/<int:term_id>'
)
api.add_resource(Auctions,
    '/auctions',
    '/auctions/'
)
api.add_resource(Exhibitions,
    '/exhibitions',
    '/exhibitions/'
)
api.add_resource(Catalog, '/catalog/<string:auction_id>')
