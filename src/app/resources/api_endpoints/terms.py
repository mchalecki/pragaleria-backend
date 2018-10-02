from typing import List, Dict, Optional

from flask_restful import Resource

from app.models import models
from consts import PRAGALERIA_UPLOAD_URL


class Terms(Resource):
    def get(self, page_number: int, page_size: int) -> List[Dict]:
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
