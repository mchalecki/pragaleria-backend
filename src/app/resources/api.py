from flask import Blueprint
from flask_restful import Resource, Api, abort

from app.models import models

api_bl = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bl)


class Terms(Resource):
    def get(self):
        try:
            all_terms = models.Terms.query.all()
        except Exception as e:
            abort(404, message="Error querying Terms. {}".format(e))
        result = []
        for term in all_terms:
            if term.term_id and term.name:
                result.append({
                    'id': term.term_id,
                    'name': term.name,
                    'description': get_term_description(term.term_id)
                })
        return result


def get_term_description(term_id):
    try:
        term_taxonomy = models.TermTaxonomies.query.filter_by(
            term_id=term_id
        ).first()
        if term_taxonomy.taxonomy == 'autor':
            return term_taxonomy.description
    except Exception as e:
        pass
    else:
        return ''


api.add_resource(Terms, '/terms')
