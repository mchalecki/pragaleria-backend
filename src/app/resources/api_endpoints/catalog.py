import phpserialize as php
from flask_restful import Resource, abort

from app.models import models
from consts import PRAGALERIA_UPLOAD_URL


class Catalog(Resource):
    def get(self, auction_id:str):
        catalog = self._get_auction_catalog(auction_id)

        result = []
        for data in self._php_meta_to_dict(catalog).values():
            result.append(self._build_auction_item(data))
        return result

    def _get_auction_catalog(self, auction_id):
        catalog = self._query_catalog(auction_id)
        if catalog is None:
            auction = models.Posts.query.filter_by(id=auction_id).first()
            catalog = self._query_catalog(auction.post_parent)
        return catalog

    @staticmethod
    def _query_catalog(post_id):
        return models.Postmeta.query.filter_by(
            post_id=post_id,
            meta_key='katalog'
        ).first()

    @staticmethod
    def _php_meta_to_dict(meta):
        return php.loads(
            php.loads(
                meta.meta_value.encode(),
                object_hook=php.phpobject
            )
        )

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

        auction_item['thumbnail'] = self._get_auction_item_url(item_id)
        auction_item['author'] = self._get_auction_item_author(item_id)

        return auction_item

    @staticmethod
    def _get_auction_item_url(item_id):
        thumbnail_id = models.Postmeta.query.filter_by(
            post_id=item_id,
            meta_key='_thumbnail_id'
        ).first()

        if thumbnail_id:
            thumbnail = models.Postmeta.query.filter_by(
                post_id=thumbnail_id.meta_value,
                meta_key='_wp_attached_file'
            ).first()

            if thumbnail:
                return f'{PRAGALERIA_UPLOAD_URL}{thumbnail.meta_value}'

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
