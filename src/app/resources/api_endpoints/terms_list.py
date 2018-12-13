from flask import request
from flask_restful import Resource, abort
from sqlalchemy import or_

from app.api_utils.caching import cache
from app.configs import current_config
from app.models import models
from app.api_utils import thumbnails


class TermsList(Resource):
    @cache.cached(timeout=current_config.CACHE_TIMEOUT)
    def get(self):
        try:
            search_query = request.args.get('search', None)
            if search_query:
                return self._handle_search(search_query)
            else:
                page_number = int(request.args.get('page') or '0')
                page_size = int(request.args.get('size') or '20')
                return self._build_data_list(page_number, page_size)
        except Exception as e:
            abort(404, message='Error querying Terms. {}'.format(e))

    def _handle_search(self, search_query):
        if len(search_query) < 3:
            return []

        filter_like = f'%{search_query}%'
        authors = models.Terms.query.filter(
            or_(
                models.Terms.name.like(filter_like),
                models.Terms.slug.like(filter_like)
            )
        ).order_by(
            models.Terms.slug
        ).all()

        result = []
        for author in authors:
            taxonomy = models.TermTaxonomies.query.filter_by(
                term_id=author.term_id,
                taxonomy='autor'
            ).first()
            if taxonomy:
                result.append(self._build_author(taxonomy))
        return result

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

            result = {}
            for artwork in relationships:
                image = thumbnails.by_id(artwork.object_id)
                if image and image['image_thumbnail']:
                    result = image
                    break

            return {
                'id': term.term_id,
                'name': term.name,
                'slug': term.slug,
                **result
            }