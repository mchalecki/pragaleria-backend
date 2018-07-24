from flask import Blueprint, jsonify
from flask_restful import Resource, Api

test_bl = Blueprint('test', __name__, url_prefix='/test')
test = Api(test_bl)


class PingResource(Resource):
    def get(self):
        return jsonify(ping="pong")


test.add_resource(PingResource, '/ping')
