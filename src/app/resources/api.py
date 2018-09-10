import json

from flask import Blueprint, make_response
from flask_restful import Resource, Api, abort
from sqlalchemy.sql import func

from app.models import models

api_bl = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bl)


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(
        json.dumps(
            data,
            ensure_ascii=False
        ).encode('utf8'),
    code)
    resp.headers.extend(headers or {})
    return resp


class Auctions(Resource):
    def get(self):
        try:
            auctions = models.Posts.query.filter(
                models.Posts.guid.like(
                    '%aukcje-wystawy%'
                )
            ).filter(
                models.Posts.post_name.like(
                    '%aukcja%'
                )
            ).order_by(models.Posts.post_date.desc())
        except Exception as e:
            abort(404, message='Error querying Posts. {}'.format(e))
        result = []
        for auction in auctions:
            if auction.post_title and auction.post_excerpt:
                result.append({
                    'id': auction.id,
                    'title': auction.post_title,
                    'description': auction.post_excerpt,
                    'guid': auction.guid,
                    'date': str(auction.post_date)
                })
        return result


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
api.add_resource(Auctions, '/auctions')
