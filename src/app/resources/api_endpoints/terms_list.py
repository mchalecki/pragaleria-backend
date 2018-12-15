from flask import request
from flask_restful import Resource, abort
from sqlalchemy import func

from app.api_utils.caching import cache
from app.configs import current_config
from app.models import models
from app.api_utils import thumbnails


class TermsList(Resource):
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

    @staticmethod
    def _handle_search(search_query):
        if len(search_query) < 2:
            return []

        filter_like = f'%{search_query.title()}%'
        authors = models.Terms.query.filter(
            models.Terms.name.like(func.binary(filter_like))
        ).order_by(
            models.Terms.slug
        ).all()

        result = []
        t8 = 0.
        for author in authors:
            taxonomy = models.TermTaxonomies.query.filter_by(
                term_id=author.term_id,
                taxonomy='autor'
            ).first()
            if taxonomy:
                result.append(TermsList._build_author(taxonomy))
        return result

    @staticmethod
    @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _build_data_list(page_number, page_size):
        result = []
        author_query = models.TermTaxonomies.query.filter_by(taxonomy='autor')
        number_of_authors = len(author_query.all())
        all_pages = number_of_authors // page_size
        page_number = max(min(page_number, all_pages), 0)
        offset_size = page_number * page_size

        if page_number == all_pages:
            return []

        for taxonomy in author_query.limit(page_size).offset(offset_size):
            author = TermsList._build_author(taxonomy)
            if author:
                result.append(author)
        return result

    @staticmethod
    @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _build_author(taxonomy):
        term = models.Terms.query.filter_by(term_id=taxonomy.term_id).first()
        if term:
            result = {
                'id': term.term_id,
                'name': term.name,
                'slug': term.slug
            }
            artwork = models.TermRelationships.query.filter(
                models.TermRelationships.term_taxonomy_id == taxonomy.term_taxonomy_id).first()
            if artwork:
                image = thumbnails.by_id(artwork.object_id)
                if image and image['image_thumbnail']:
                    result = {**result, **image}

            return result
