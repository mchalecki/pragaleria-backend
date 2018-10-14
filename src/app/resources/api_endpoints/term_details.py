
from flask_restful import Resource, abort

from app.models import models
from app.api_utils import thumbnails, postmeta


class TermDetails(Resource):
    def get(self, term_id=None):
        try:
            return self.build_object(term_id)
        except Exception as e:
            abort(404, message='Error querying TermDetails. {}'.format(e))

    def build_object(self, term_id):
        if not term_id:
            return None

        term, relationships = self._get_term_with_relationships(term_id)

        if term and relationships and len(relationships) > 0:
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
        term = models.Terms.query.filter_by(
            term_id=term_id
        ).first()

        relationships = models.TermRelationships.query.filter_by(
            term_taxonomy_id=term_id
        ).all()

        return term, relationships

    def _get_author_artwork_from_post(self, artwork):
        artwork_id = artwork.object_id
        artwork_post = models.Posts.query.filter_by(
            id=artwork_id
        ).first()

        if artwork_post:
            return {
                'id': artwork_id,
                'title': artwork_post.post_title,
                'description': artwork_post.post_content,
                'sold': postmeta.by_key(artwork_id, 'oferta_status'),
                'initial_price': postmeta.by_key(artwork_id, 'oferta_cena'),
                'price': postmeta.by_key(artwork_id, 'oferta_cena_sprzedazy'),
                'year': postmeta.by_key(artwork_id, 'oferta_rok'),
                'thumbnail': thumbnails.by_id(artwork_id)
            }
        
        return {}
