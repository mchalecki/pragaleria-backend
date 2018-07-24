from flask import Blueprint
from flask_restful import Api

api_bl = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bl)
