from flask import request
from flask_restful import Resource, abort

from app.models import models
from app.api_utils import thumbnails, postmeta


class TermsList(Resource):
    def get(self): # mozna przetestowac czy jest 404 jak bledne argumenty podaje
        try:
            page_number = int(request.args.get('page') or '0')
            page_size = int(request.args.get('size') or '20')
            return self._build_data_list(page_number, page_size)
        except Exception as e:
            abort(404, message='Error querying Terms. {}'.format(e))

    def _build_data_list(self, page_number, page_size):
        result = []
        author_query = models.TermTaxonomies.query.filter_by(taxonomy='autor')
        number_of_authors = len(author_query.all())
        all_pages = number_of_authors // page_size
        page_number = max(min(page_number, all_pages), 0)
        offset_size = page_number * page_size

        if page_number == all_pages:
            return []

        for taxonomy in author_query.limit(page_size).offset(offset_size):
            author = self._build_author(taxonomy)
            if author:
                result.append(author)
        return result

    def _build_author(self, taxonomy):
        term = models.Terms.query.filter_by(term_id=taxonomy.term_id).first()
        if term:
            relationships = models.TermRelationships.query.filter_by(
                term_taxonomy_id=taxonomy.term_taxonomy_id).all()

            result = ''
            for artwork in relationships:
                image = thumbnails.by_id(artwork.object_id)
                if image and image['image_thumbnail']:
                    result = image['image_thumbnail']
                    break

            return {
                'id': term.term_id,
                'name': term.name,
                'slug': term.slug,
                'image_thumbnail': result
            }