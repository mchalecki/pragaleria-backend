from flask_restful import Resource, abort

from app.models import models
from app.api_utils import thumbnails, postmeta


class TermDetails(Resource):
    def get(self, term_id=None):
        if term_id is not None:
            author = self.build_object(term_id)
            if author:
                return author

        abort(404, message='Author does not exist. id: {}'.format(term_id))

    def build_object(self, term_id):
        term, relationships, taxonomy = self._get_term_details(term_id)
        if term and taxonomy and relationships and len(relationships) > 0:
            result = {}
            result['id'] = term_id
            result['name'] = getattr(term, 'name', '')
            result['slug'] = getattr(term, 'slug', '')
            result['description'] = getattr(taxonomy, 'description', '')
            artworks = self._build_artworks(relationships)
            result['artworks'] = artworks
            result['image_thumbnail'] = ''
            if len(artworks) > 0:
                result['image_thumbnail'] = artworks[0]['image_thumbnail']

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
            relationships = None

        return term, relationships, taxonomy

    def _build_artworks(self, artwork_candidates):
        artworks, titles = [], []
        for artwork in artwork_candidates:
            artwork_id = artwork.object_id
            artwork_post = models.Posts.query.filter_by(
                id=artwork_id
            ).first()
            if artwork_post and hasattr(artwork_post, 'post_title'):
                if artwork_post.post_title not in titles:
                    titles.append(artwork_post.post_title)
                    artworks.append(self._get_artwork_from_post(artwork_post))
        return artworks

    def _get_artwork_from_post(self, artwork_post):
        artwork_id = artwork_post.id

        result = {}

        result['id'] = artwork_id
        result['title'] = getattr(artwork_post, 'post_title', '')
        result['description'] = getattr(artwork_post, 'post_content', '')
        result['sold'] = bool(int(postmeta.by_key(artwork_id, 'oferta_status', '0')))
        result['initial_price'] = postmeta.by_key(artwork_id, 'oferta_cena', '')
        result['sold_price'] = postmeta.by_key(artwork_id, 'oferta_cena_sprzedazy', '')
        result['year'] = postmeta.by_key(artwork_id, 'oferta_rok', '')

        image = thumbnails.by_id(artwork_id)
        result['image_original'] = image['image_original']
        result['image_thumbnail'] = image['image_thumbnail']

        return result