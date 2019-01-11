import time

from flask import current_app, request
from flask_restful import Resource, abort

from app.api_utils.caching import cache
from app.api_utils.string_utils import get_dimensions_from_description
from app.configs import current_config
from app.models import models
from app.api_utils import postmeta, phpmeta, thumbnails, html_utils


class Catalog(Resource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, auction_id: str):
        catalog = Catalog._get_auction_catalog(auction_id)
        if not catalog:
            abort(404, message='Catalog for this auction does not exist. id: {}'.format(auction_id))
        result = Catalog.generate_response(catalog)
        sold = request.args.get('sold', None)
        if sold:
            if sold == 'true':
                result = [i for i in result if i.get("sold", None) is True]
            elif sold == 'false':
                result = [i for i in result if i.get("sold", None) is False]
        return result

    @staticmethod
    @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def generate_response(catalog):
        result = []
        for data in phpmeta.to_dict(catalog).values():
            auction_item = Catalog._build_auction_item(data)
            description = auction_item.get('description', '')
            dimensions = get_dimensions_from_description(description)
            auction_item["meta"] = {"dimension": dimensions}
            result.append(auction_item)
        return result

    @staticmethod
    def _get_auction_catalog(auction_id):
        catalog = postmeta.by_key(auction_id, 'katalog')
        if catalog is None:
            auction = models.Posts.query.filter_by(id=auction_id).first()
            if auction:
                catalog = postmeta.by_key(auction.post_parent, 'katalog')
        return catalog

    @staticmethod
    def _build_auction_item(data):
        item_id = int(data['id'])
        item_post = models.Posts.query.filter_by(id=item_id).first()

        auction_item = {
            'id': item_id,
            'title': item_post.post_title,
            'description': html_utils.clean(item_post.post_content),
            'initial_price': '',
            'sold_price': '',
            'after_auction_price': '',
            'sold': False,
            'author': '',
            'author_id': '',
            **thumbnails.by_id(item_id)
        }

        if 'cena_wywolawcza' in data.keys():
            auction_item['initial_price'] = data['cena_wywolawcza']
        if 'cena_poaukcyjna' in data.keys():
            auction_item['after_auction_price'] = data['cena_poaukcyjna']
        if 'cena_sprzedazy' in data.keys():
            auction_item['sold_price'] = data['cena_sprzedazy']
        if 'sprzedana' in data.keys():
            auction_item['sold'] = bool(int(data['sprzedana']))

        item_author = Catalog._get_auction_item_author(item_id)
        if item_author:
            auction_item['author_id'] = item_author.term_id
            auction_item['author'] = item_author.name

        return auction_item

    @staticmethod
    def _get_auction_item_author(item_id):
        relationships = models.TermRelationships.query.filter_by(
            object_id=item_id).all()

        for relationship in relationships:
            author = models.TermTaxonomies.query.filter_by(
                term_taxonomy_id=relationship.term_taxonomy_id,
                taxonomy='autor'
            ).first()

            if author:
                return models.Terms.query.filter_by(
                    term_id=author.term_id
                ).first()

        return ''
