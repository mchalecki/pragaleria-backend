
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

        term, relationships, taxonomy = self._get_term_details(term_id)

        if term and relationships and len(relationships) > 0:
            result = {}

            result['id'] = term_id

            if hasattr(term, 'name'):
                result['name'] = term.name

            if hasattr(term, 'slug'):
                result['slug'] = term.slug

            if hasattr(taxonomy, 'description'):
                result['description'] = taxonomy.description

            artworks = map(self._get_author_artwork_from_post, relationships)
            if artworks:
                result['artworks'] = list(artworks)

            return result

    def _get_term_details(self, term_id):
        term = models.Terms.query.filter_by(
            term_id=term_id
        ).first()

        taxonomy = models.TermTaxonomies.query.filter_by(
            term_id=term_id,
        ).first()

        relationships = models.TermRelationships.query.filter_by(
            term_taxonomy_id=taxonomy.term_taxonomy_id
        ).all()

        return term, relationships, taxonomy

    def _get_author_artwork_from_post(self, artwork):
        artwork_id = artwork.object_id
        artwork_post = models.Posts.query.filter_by(
            id=artwork_id
        ).first()

        result = {}

        if artwork_post:

            result['id'] = artwork_id

            if hasattr(artwork_post, 'post_title'):
                result['title'] = artwork_post.post_title

            if hasattr(artwork_post, 'post_content'):
                result['description'] = artwork_post.post_content

            sold = postmeta.by_key(artwork_id, 'oferta_status')
            if sold and sold.isdigit():
                result['description'] = bool(int(sold))

            initial_price = postmeta.by_key(artwork_id, 'oferta_cena')
            if initial_price:
                result['initial_price'] = initial_price

            sold_price = postmeta.by_key(artwork_id, 'oferta_cena_sprzedazy')
            if sold_price:
                result['sold_price'] = sold_price

            year = postmeta.by_key(artwork_id, 'oferta_rok')
            if year and year.isdigit():
                result['year'] = int(year)

            thumbnail = thumbnails.by_id(artwork_id)
            if thumbnail:
                result['thumbnail'] = thumbnail

        return result