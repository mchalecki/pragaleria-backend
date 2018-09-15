import json
import phpserialize as php

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
            return self._build_auctions_list()
        except Exception as e:
            abort(404, message='Error querying Posts. {}'.format(e))

    def _build_auctions_list(self):
        result = []
        for parent in self._query_auctions():
            revision = models.Posts.query.filter_by(
                post_parent=parent.id
            ).order_by(models.Posts.post_modified.desc()).first()
            data = revision or parent
            if data.post_title and data.post_excerpt:
                result.append(self._build_auction(parent, revision))

        return result

    def _query_auctions(self):
        return models.Posts.query.filter(
            models.Posts.guid.like('%aukcje-wystawy%')
        ).filter(
            models.Posts.post_name.like('%aukcja%')
        ).order_by(models.Posts.post_modified.desc())

    def _build_auction(self, parent, revision):
        auction_data = {}

        data = revision or parent

        auction_data['id'] = data.id
        auction_data['title'] = data.post_title
        auction_data['description'] = data.post_excerpt
        auction_data['guid'] = data.guid
        auction_data['date'] = str(data.post_modified)

        auction_data['auction_start'] = self._query_postmeta_by_key(
            parent.id, 'aukcja_start')
        auction_data['auction_end'] = self._query_postmeta_by_key(
            parent.id, 'aukcja_end')
        auction_data['auction_status'] = self._query_postmeta_by_key(
            parent.id, 'aukcja_status')

        return auction_data

    def _query_postmeta_by_key(self, post_id, key):
        result = models.Postmeta.query.filter_by(
            post_id=post_id,
            meta_key=key
        ).first()

        if result:
            return result.meta_value


class AuctionCatalog(Resource):
    def get(self, auction_id):
        try:
            catalog = self._get_auction_catalog(auction_id)
            result = []
            for data in self._php_meta_to_dict(catalog).values():
                result.append(self._build_auction_item(data))
            return result
        except Exception as e:
            abort(404, message='Error querying Postmeta. {}'.format(e))

    def _get_auction_catalog(self, auction_id):
        catalog = self._query_catalog(auction_id)
        if catalog is None:
            auction = models.Posts.query.filter_by(id=auction_id).first()
            catalog = self._query_catalog(auction.post_parent)
        return catalog

    def _query_catalog(self, post_id):
        return models.Postmeta.query.filter_by(
            post_id=post_id,
            meta_key='katalog'
        ).first()

    def _php_meta_to_dict(self, meta):
        return php.loads(
            php.loads(
                meta.meta_value.encode(),
                object_hook=php.phpobject
            )
        )

    def _build_auction_item(self, data):
        item_id = data[b'id'].decode()
        item_post = models.Posts.query.filter_by(id=item_id).first()

        auction_item = {}

        auction_item['id'] = item_id
        auction_item['title'] = item_post.post_title
        auction_item['description'] = item_post.post_content

        auction_item['catalog_number'] = data[b'katalog_nr'].decode()
        auction_item['initial_price'] = data[b'cena_wywolawcza'].decode()
        auction_item['sold_price'] = data[b'cena_sprzedazy'].decode()
        auction_item['after_auction_price'] = data[b'cena_poaukcyjna'].decode()
        auction_item['sold'] = data[b'sprzedana'].decode()

        auction_item['thumbnail'] = self._get_auction_item_url(item_id)
        auction_item['author'] = self._get_auction_item_author(item_id)

        return auction_item

    def _get_auction_item_url(self, item_id):
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
                return f'http://pragaleria.pl/wp-content/uploads/{thumbnail.meta_value}'

    def _get_auction_item_author(self, item_id):
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
api.add_resource(AuctionCatalog, '/auctions/<string:auction_id>')
