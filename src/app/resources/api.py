import json
import phpserialize as php

from flask import Blueprint, make_response
from flask_restful import Resource, Api, abort

from sqlalchemy.sql import func
from sqlalchemy import not_

from app.models import models


PRAGALERIA_UPLOAD_URL = 'http://pragaleria.pl/wp-content/uploads/'
PRAGALERIA_AUCTIONS_URL = 'http://pragaleria.pl/aukcje-wystawy/'

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


class PostsBaseApi(Resource):
    def get(self):
        try:
            return self._build_data_list()
        except Exception as e:
            abort(404, message='Error querying Posts. {}'.format(e))
    
    def _build_data_list(self):
        raise NotImplementedError

    def _query_posts(self):
        raise NotImplementedError

    def _build_post(self, parent, revision):
        post_data = {}

        data = revision or parent

        post_data['id'] = data.id
        post_data['title'] = data.post_title
        post_data['description_content'] = data.post_content
        post_data['description_excerpt'] = data.post_excerpt
        post_data['guid'] = f'{PRAGALERIA_AUCTIONS_URL}{parent.post_name}'
        post_data['date'] = str(data.post_modified)

        post_data['auction_start'] = self._query_postmeta_by_key(
            parent.id, 'aukcja_start')
        post_data['auction_end'] = self._query_postmeta_by_key(
            parent.id, 'aukcja_end')
        post_data['auction_status'] = self._query_postmeta_by_key(
            parent.id, 'aukcja_status')

        post_data['thumbnail'] = self._get_thumbnail(parent.id)

        return post_data

    def _query_postmeta_by_key(self, post_id, key):
        result = models.Postmeta.query.filter_by(
            post_id=post_id,
            meta_key=key
        ).first()

        if result:
            return result.meta_value

    def _get_thumbnail(self, item_id):
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


class Auctions(PostsBaseApi):
    def _query_posts(self):
        return models.Posts.query.filter(
            models.Posts.guid.like('%aukcje-wystawy%')
        ).filter(
            models.Posts.post_name.like('%aukcja%')
        ).order_by(models.Posts.post_modified.desc())

    def _build_data_list(self):
        result = []
        for parent in self._query_posts():
            revision = models.Posts.query.filter_by(
                post_parent=parent.id
            ).order_by(models.Posts.post_modified.desc()).first()
            data = revision or parent
            if data.post_title and (data.post_excerpt or data.post_content):
                result.append(self._build_post(parent, revision))

        return result


class Exhibitions(PostsBaseApi):
    def _query_posts(self):
        return models.Posts.query.filter(
            models.Posts.guid.like('%/aukcje-wystawy/%'),
            models.Posts.post_status == 'publish'
        ).filter(
            not_(
                models.Posts.post_name.like('%aukcja%')
            )
        ).order_by(models.Posts.post_modified.desc())

    def _build_data_list(self):
        result = []
        for parent in self._query_posts():
            if parent.post_title:
                result.append(self._build_post(parent, parent))

        return result


class Catalog(Resource):
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
                return f'{PRAGALERIA_UPLOAD_URL}{thumbnail.meta_value}'

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
    def get(self, page_number):
        try:
            result = []
            author_query = models.TermTaxonomies.query.filter_by(taxonomy='autor')
            page_size = 20
            all_pages = len(author_query.all()) // page_size
            if page_number < 0:
                page_number = 0
    
            if page_number > all_pages:
                page_number = all_pages
            
            current_taxonomies = author_query.limit(page_size).offset(page_number * page_size)
            for taxonomy in current_taxonomies:
                author = self._build_author(taxonomy)
                if author:
                    result.append(author)
            return result
        except Exception as e:
            abort(404, message="Error querying Terms. {}".format(e))
    
    def _build_author(self, taxonomy):
        term = models.Terms.query.filter_by(term_id=taxonomy.term_id).first()
        if term:
            relationship = models.TermRelationships.query.filter_by(
                term_taxonomy_id=taxonomy.term_taxonomy_id).first()
            if relationship:
                thumbnail = self._get_thumbnail(relationship.object_id)
                if thumbnail:
                    return {
                        'id': term.term_id,
                        'name': term.name,
                        'slug': term.slug,
                        'thumbnail': thumbnail
                    }

    def _get_thumbnail(self, item_id):
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


api.add_resource(Terms, '/terms/<int:page_number>')
api.add_resource(Auctions, '/auctions')
api.add_resource(Exhibitions, '/exhibitions')
api.add_resource(Catalog, '/catalog/<string:auction_id>')
