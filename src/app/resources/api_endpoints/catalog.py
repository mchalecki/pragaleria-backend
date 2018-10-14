import phpserialize as php
from flask_restful import Resource, abort

from app.models import models
from app.api_utils import postmeta, phpmeta, thumbnails


class Catalog(Resource):
    def get(self, auction_id:str):
        catalog = self._get_auction_catalog(auction_id)

        result = []
        for data in phpmeta.to_dict(catalog).values():
            result.append(self._build_auction_item(data))
        return result

    def _get_auction_catalog(self, auction_id):
        catalog = postmeta.by_key(auction_id, 'katalog')
        if catalog is None:
            auction = models.Posts.query.filter_by(id=auction_id).first()
            catalog = postmeta.by_key(auction.post_parent, 'katalog')
        return catalog

    def _build_auction_item(self, data):
        item_id = data[b'id'].decode()
        item_post = models.Posts.query.filter_by(id=item_id).first()

        auction_item = {'id': item_id, 'title': item_post.post_title, 'description': item_post.post_content}

        if data[b'katalog_nr']:
            auction_item['catalog_number'] = data[b'katalog_nr'].decode()

        if data[b'cena_wywolawcza']:
            auction_item['initial_price'] = data[b'cena_wywolawcza'].decode()

        if data[b'cena_sprzedazy']:
            auction_item['sold_price'] = data[b'cena_sprzedazy'].decode()

        if data[b'cena_poaukcyjna']:
            auction_item['after_auction_price'] = data[b'cena_poaukcyjna'].decode()

        if data[b'sprzedana']:
            auction_item['sold'] = data[b'sprzedana'].decode()

        auction_item['thumbnail'] = thumbnails.by_id(item_id)
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
