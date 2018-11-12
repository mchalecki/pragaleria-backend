import re

import phpserialize as php
from flask_restful import Resource, abort

from app.models import models
from app.api_utils import postmeta, phpmeta, thumbnails


class Catalog(Resource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dimension_regex = re.compile(r"(\d+(,\d)?(\s?x\s?)?)+")

    def get(self, auction_id: str):
        catalog = self._get_auction_catalog(auction_id)

        if not catalog:
            abort(404, message='Catalog for this auction does not exist. id: {}'.format(auction_id))

        result = []
        for data in phpmeta.to_dict(catalog).values():
            auction_item = self._build_auction_item(data)
            description = auction_item.get('description', '')
            dimensions = self.dimension_regex.search(description)
            if dimensions:
                dimensions = dimensions.group()
                dimensions = dimensions.replace(' ', '').split('x')
                if len(dimensions) >= 2:
                    auction_item["meta"] = {"dimension": dimensions}  # TODO add handling exceptions
            result.append(auction_item)
        return result

    def _get_auction_catalog(self, auction_id):
        catalog = postmeta.by_key(auction_id, 'katalog')
        if catalog is None:
            auction = models.Posts.query.filter_by(id=auction_id).first()
            if auction:
                catalog = postmeta.by_key(auction.post_parent, 'katalog')
        return catalog

    def _build_auction_item(self, data):
        item_id = int(data['id'])
        item_post = models.Posts.query.filter_by(id=item_id).first()

        auction_item = {
            'id': item_id,
            'title': item_post.post_title,
            'description': item_post.post_content,
            'initial_price': '',
            'sold_price': '',
            'after_auction_price': '',
            'sold': False,
            'image_thumbnail': '',
            'image_original': '',
            'author': ''
        }

        if data['cena_wywolawcza']:
            auction_item['initial_price'] = data['cena_wywolawcza']

        if data['cena_sprzedazy']:
            auction_item['sold_price'] = data['cena_sprzedazy']

        if data['cena_poaukcyjna']:
            auction_item['after_auction_price'] = data['cena_poaukcyjna']

        if data['sprzedana']:
            auction_item['sold'] = bool(int(data['sprzedana']))

        image = thumbnails.by_id(item_id)
        if image:
            auction_item['image_original'] = image['image_original']
            auction_item['image_thumbnail'] = image['image_thumbnail']

        auction_item['author'] = self._get_auction_item_author(item_id)

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
                ).first().name

        return ''
