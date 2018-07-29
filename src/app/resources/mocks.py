import json

from flask import Blueprint
from flask_restful import Resource, Api

from paths import STATIC

mocks_bl = Blueprint('mocks', __name__, url_prefix='/mocks')
mocks = Api(mocks_bl)


class MockArtists(Resource):
    def get(self):
        with open(STATIC.MOCKS.ARTISTS) as f:
            data = json.load(f)
            return data


mocks.add_resource(MockArtists, '/artists')
