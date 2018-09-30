from typing import List, Dict, Optional

from flask_restful import Resource, abort

from app.models import models
from consts import PRAGALERIA_UPLOAD_URL


class TermsList(Resource):
    def get(self, page_number: int=0, page_size: int=20) -> List[Dict]:
        result = []
        author_query = models.TermTaxonomies.query.filter_by(taxonomy='autor')
        all_pages = len(author_query.all()) // page_size
        page_number = max(min(page_number, all_pages), 0)

        current_taxonomies = author_query.limit(page_size).offset(page_number * page_size)
        for taxonomy in current_taxonomies:
            author = self._build_author(taxonomy)
            if author:
                result.append(author)
        return result

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

    @staticmethod
    def _get_thumbnail(item_id: int) -> Optional[str]:
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


class TermDetails(Resource):
    def get(self, term_id=None):
        try:
            return self.build_object(term_id)
        except Exception as e:
            abort(404, message='Error querying Terms. {}'.format(e))

    def build_object(self, term_id):
        if not term_id:
            return None

        term, relationships = self._get_term_with_relationships(term_id)

        if not term or len(relationships) == 0:
            return None

        return {
            'id': term.term_id,
            'name': term.name,
            'slug': term.slug,
            'artworks': list(map(
                self._get_author_artwork_from_post,
                relationships
            ))
        }

    def _get_term_with_relationships(self, term_id):
        # Relationships correspond to each object
        # which Term is the author of (say 'artwork').
        # Each object has a corresponding Post /w Postmeta.
        term = models.Terms.query.filter_by(
            term_id=term_id
        ).first()

        relationships = models.TermRelationships.query.filter_by(
            term_taxonomy_id=term_id
        ).all()

        return term, relationships

    def _get_author_artwork_from_post(self, artwork):
        result = {}

        artwork_id = artwork.object_id
        artwork_post = models.Posts.query.filter_by(
            id=artwork_id
        ).first()

        if not artwork_post:
            return result

        return {
            'id': artwork_id,
            'title': artwork_post.post_title,
            'description': artwork_post.post_content,
            'sold': self._get_postmeta_by_key(artwork_id, 'oferta_status'),
            'initial_price': self._get_postmeta_by_key(artwork_id, 'oferta_cena'),
            'price': self._get_postmeta_by_key(artwork_id, 'oferta_cena_sprzedazy'),
            'year': self._get_postmeta_by_key(artwork_id, 'oferta_rok'),
            'thumbnail': self._get_thumbnail(artwork_id)
        }

    def _get_postmeta_by_key(self, item_id, meta_key):
        postmeta = models.Postmeta.query.filter_by(
            post_id=item_id,
            meta_key=meta_key
        ).first()

        if not postmeta:
            return None
        else:
            return postmeta.meta_value

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
