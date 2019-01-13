from flask import current_app, request
from flask_restful import Resource, abort
from sqlalchemy import func

from app.api_utils.caching import cache
from app.api_utils.phpmeta import to_dict
from app.api_utils.string_utils import get_dimensions_from_description, string_to_bool
from app.configs import current_config
from app.models import models
from app.api_utils import thumbnails, postmeta, html_utils
from app.api_utils.base_post_api import BasePostApi


class ArtworksList(Resource):
    def get(self):
        try:
            search_query = request.args.get('search', None)
            tags_query = request.args.get('tags', None)

            if tags_query and search_query:
                return self._handle_tags_search(tags_query, search_query)

            if search_query:
                return self._handle_search(search_query)

            page_number = int(request.args.get('page') or '0')
            page_size = int(request.args.get('size') or '20')

            if tags_query:
                return self._handle_tags(tags_query, page_number, page_size)

            return self._build_data_list(page_number, page_size)
        except Exception as e:
            abort(404, message='Error querying Artworks. {}'.format(e))

    @staticmethod
    # @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _handle_tags_search(tags_query, search_query):
        if not tags_query.isdigit():
            return []

        tags_query = int(tags_query)

        if tags_query not in [12, 145, 231, 233, 235, 1385]:
            return []

        if len(search_query) < 3:
            return []

        filter_like = f'%{search_query.title()}%'
        artworks = models.Posts.query.filter(
            models.Posts.post_title.like(func.binary(filter_like)),
            models.Posts.post_type == 'oferta',
            models.Posts.guid.like('%/oferta/%'),
        ).order_by(
            models.Posts.post_name
        )

        result = []
        titles = []
        indices = []

        for artwork_m in artworks:
            taxonomies = models.TermRelationships.query.filter_by(
                object_id=artwork_m.id,
                term_taxonomy_id=int(tags_query)
            ).first()
            if taxonomies:
                artwork = ArtworksList._get_artwork_from_post(artwork_m)
                if artwork['title'] in titles:
                    index = titles.index(artwork['title'])
                    if artwork['id'] > indices[index]:
                        indices[index] = artwork['id']
                        titles[index] = artwork['title']
                        result[index] = artwork
                else:
                    indices.append(artwork['id'])
                    titles.append(artwork['title'])
                    result.append(artwork)
        return result

    @staticmethod
    # @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _handle_tags(tags_query, page_number, page_size):
        # 12 malarstwo
        # 145 rzezba
        # 231 grafika-warsztatowa
        # 233 grafika-cyfrowa
        # 235 grafika-wektorowa
        # 1385 ceramika

        if not tags_query.isdigit():
            return []

        tags_query = int(tags_query)

        if tags_query not in [12, 145, 231, 233, 235, 1385]:
            return []

        artwork_query = models.TermRelationships.query.filter_by(
            term_taxonomy_id=int(tags_query)
        )
        number_of_artworks = len(artwork_query.all())
        all_pages = number_of_artworks // page_size
        offset_size = page_number * page_size

        if page_number > all_pages:
            return []

        result = []
        titles = []
        indices = []

        for artwork_m in artwork_query.limit(page_size).offset(offset_size):
            post = models.Posts.query.filter_by(
                id=artwork_m.object_id
            ).first()
            artwork = ArtworksList._get_artwork_from_post(post)
            if artwork['title'] in titles:
                index = titles.index(artwork['title'])
                if artwork['id'] > indices[index]:
                    indices[index] = artwork['id']
                    titles[index] = artwork['title']
                    result[index] = artwork
            else:
                indices.append(artwork['id'])
                titles.append(artwork['title'])
                result.append(artwork)

        return result

    @staticmethod
    # @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _handle_search(search_query):
        if len(search_query) < 3:
            return []

        filter_like = f'%{search_query.title()}%'
        artworks = models.Posts.query.filter(
            models.Posts.post_title.like(func.binary(filter_like)),
            models.Posts.post_type == 'oferta',
            models.Posts.guid.like('%/oferta/%'),
        ).order_by(
            models.Posts.post_name
        )

        result = []
        titles = []
        indices = []

        for artwork_m in artworks:
            artwork = ArtworksList._get_artwork_from_post(artwork_m)
            if artwork['title'] in titles:
                index = titles.index(artwork['title'])
                if artwork['id'] > indices[index]:
                    indices[index] = artwork['id']
                    titles[index] = artwork['title']
                    result[index] = artwork
            else:
                indices.append(artwork['id'])
                titles.append(artwork['title'])
                result.append(artwork)
        return result

    @staticmethod
    # @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _build_data_list(page_number, page_size):

        artwork_query = models.Posts.query.filter(
            models.Posts.post_type == 'oferta',
            models.Posts.guid.like('%/oferta/%'),
        )

        number_of_artworks = len(artwork_query.all())
        all_pages = number_of_artworks // page_size
        page_number = max(min(page_number, all_pages), 0)
        offset_size = page_number * page_size

        if page_number == all_pages:
            return []

        result = []
        titles = []
        indices = []

        for artwork_m in artwork_query.limit(page_size).offset(offset_size):
            artwork = ArtworksList._get_artwork_from_post(artwork_m)
            if artwork['title'] in titles:
                index = titles.index(artwork['title'])
                if artwork['id'] > indices[index]:
                    indices[index] = artwork['id']
                    titles[index] = artwork['title']
                    result[index] = artwork
            else:
                indices.append(artwork['id'])
                titles.append(artwork['title'])
                result.append(artwork)

        return result

    @staticmethod
    def _get_artwork_from_post(artwork_post):
        artwork_id = artwork_post.id

        taxonomies = models.TermRelationships.query.filter_by(
            object_id=artwork_id
        ).all()

        author_id = ''
        author_name = ''
        tags = []

        for taxonomy in taxonomies:
            taxonomy_id = taxonomy.term_taxonomy_id
            taxonomy = models.TermTaxonomies.query.filter_by(
                term_taxonomy_id=taxonomy_id
            ).first()
            if taxonomy:
                term = models.Terms.query.filter_by(
                    term_id=taxonomy.term_id
                ).first()
                if taxonomy.taxonomy == 'autor':
                    author_name = term.name
                    author_id = term.term_id
                else:
                    tags.append(term.name)

        description = html_utils.clean(getattr(artwork_post, 'post_content', ''))
        dimensions = {}
        if description:
            dimensions = get_dimensions_from_description(description)
        result = {
            'id': artwork_id,
            'title': getattr(artwork_post, 'post_title', ''),
            'author_id': author_id,
            'author': author_name,
            'tags': tags,
            'description': html_utils.clean(getattr(artwork_post, 'post_content', '')),
            'year': postmeta.by_key(artwork_id, 'oferta_rok', ''),
            'meta': {'dimension': dimensions},
            **thumbnails.by_id(artwork_id),
        }
        sold_info = ArtworksList._get_artwork_from_postmeta(artwork_id) or {}

        return {
            **result,
            **sold_info
        }

    @staticmethod
    def _get_artwork_from_postmeta(artwork_id):
        sold = postmeta.by_key(artwork_id, 'oferta_status', '0')
        initial_price = postmeta.by_key(artwork_id, 'oferta_cena', '')
        sold_price = postmeta.by_key(artwork_id, 'oferta_cena_sprzedazy', '')

        if not all([sold, initial_price, sold_price]):
            catalog_data = models.Postmeta.query.filter(
                models.Postmeta.meta_key == 'katalog',
                models.Postmeta.meta_value.like(f'%:"{artwork_id}";%')
            ).first()

            if catalog_data:
                _post = models.Posts.query.filter_by(
                    id=catalog_data.post_id
                ).first()
                meta_val = to_dict(catalog_data.meta_value)
                for d in meta_val.values():
                    if isinstance(d, dict) and 'id' in d and d['id'] == str(artwork_id):
                        return {
                            'catalog_id': catalog_data.post_id,
                            'catalog_name': _post.post_title,
                            'sold': string_to_bool(d.get('sprzedana', '0')),
                            'initial_price': d.get('cena_wywolawcza', ''),
                            'sold_price': d.get('cena_sprzedazy', ''),
                            'after_auction_price': d.get('cena_poaukcyjna', ''),
                        }

        return {
            'sold': string_to_bool(sold),
            'initial_price': initial_price,
            'sold_price': sold_price
        }
