from flask import current_app
from flask_restful import Resource, abort

from app.api_utils.caching import cache
from app.api_utils.phpmeta import to_dict
from app.api_utils.string_utils import get_dimensions_from_description, string_to_bool
from app.configs import current_config
from app.models import models
from app.api_utils import thumbnails, postmeta, html_utils


class TermDetails(Resource):
    # @cache.cached(timeout=current_config.CACHE_TIMEOUT)
    def get(self, term_id=None):
        if term_id is not None:
            author = self.build_object(term_id)
            if author:
                return author

        abort(404, message='Author does not exist. id: {}'.format(term_id))

    def build_object(self, term_id):
        term, relationships, taxonomy = self._get_term_details(term_id)
        if term and taxonomy:
            term_name = getattr(term, 'name', '')
            artworks = self._build_artworks(
                artwork_candidates=relationships,
                term_name=term_name
            )
            result = {
                'id': term_id,
                'name': term_name,
                'slug': getattr(term, 'slug', ''),
                'description': html_utils.clean(getattr(taxonomy, 'description', '')),
                'artworks': artworks,
                'image_thumbnail': ''
            }
            if len(artworks) > 0:
                result['image_thumbnail'] = artworks[0]['image_thumbnail']
                for artwork in artworks:
                    description = artwork.get('description', '')
                    dimensions = get_dimensions_from_description(description)
                    artwork["meta"] = {"dimension": dimensions}
            return result

    def _get_term_details(self, term_id):
        term = models.Terms.query.filter_by(
            term_id=term_id
        ).first()
        taxonomy = models.TermTaxonomies.query.filter_by(
            term_id=term_id,
        ).first()
        if taxonomy:
            relationships = models.TermRelationships.query.filter_by(
                term_taxonomy_id=taxonomy.term_taxonomy_id
            ).all()
        else:
            relationships = []

        return term, relationships, taxonomy

    def _build_artworks(self, artwork_candidates, term_name=''):
        artworks, titles = [], []
        for artwork in artwork_candidates:
            artwork_id = artwork.object_id
            artwork_post = models.Posts.query.filter_by(
                id=artwork_id
            ).first()
            if artwork_post and hasattr(artwork_post, 'post_title'):
                if artwork_post.post_title not in titles:
                    titles.append(artwork_post.post_title)
                    artworks.append(
                        self._get_artwork_from_post(
                            artwork_post=artwork_post,
                            term_name=term_name
                        )
                    )
        return artworks

    def _get_artwork_from_post(self, artwork_post, term_name=''):
        # sometimes artwork has postmeta "katalog" in which it was present
        # this can help when displaying artist featured in auctions
        artwork_id = artwork_post.id

        result = {
            'id': artwork_id,
            'title': getattr(artwork_post, 'post_title', ''),
            'author': term_name,
            'description': html_utils.clean(getattr(artwork_post, 'post_content', '')),
            'year': postmeta.by_key(artwork_id, 'oferta_rok', ''),
            **thumbnails.by_id(artwork_id),
        }

        sold = models.Postmeta.query.filter_by(
            post_id=artwork_id,
            meta_key='oferta_status'
        ).first()
        if sold:
            result = {
                **result,
                'sold': string_to_bool(sold),
                'initial_price': postmeta.by_key(artwork_id, 'oferta_cena', ''),
                'sold_price': postmeta.by_key(artwork_id, 'oferta_cena_sprzedazy', ''),
            }
        else:
            data = models.Postmeta.query.filter(
                models.Postmeta.meta_value.like(f'%{artwork_id}%')
            ).first()  # TODO perhaps not only first
            sold_info = {
                # Defaults
                'sold': True,
                'initial_price': '',
                'sold_price': '',
            }
            if data:
                meta_val = to_dict(data.meta_value)
                for d in meta_val.values():
                    if isinstance(d, dict) and 'id' in d and d['id'] == str(artwork_id):
                        sold_info = {
                            'sold': d.get('sprzedana', 1),
                            'initial_price': d.get('cena_wywolawcza', ''),
                            'sold_price': d.get('cena_sprzedazy', '')
                        }
                        break
                result = {
                    **result,
                    **sold_info
                }
        return result
