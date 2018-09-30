from flask_restful import Resource, abort

from app.models import models
from consts import PRAGALERIA_AUCTIONS_URL, PRAGALERIA_UPLOAD_URL


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
        data = revision or parent
        return {
            'id': data.id,
            'title': data.post_title,
            'description_content': data.post_content,
            'description_excerpt': data.post_excerpt,
            'guid': f'{PRAGALERIA_AUCTIONS_URL}{parent.post_name}',
            'date': str(data.post_modified),
            'auction_start': self._query_postmeta_by_key(parent.id, 'aukcja_start'),
            'auction_end': self._query_postmeta_by_key(parent.id, 'aukcja_end'),
            'auction_status': self._query_postmeta_by_key(parent.id, 'aukcja_status'),
            'thumbnail': self._get_thumbnail(parent.id)
        }

    @staticmethod
    def _query_postmeta_by_key(post_id, key):
        result = models.Postmeta.query.filter_by(
            post_id=post_id,
            meta_key=key
        ).first()

        if result:
            return result.meta_value

    @staticmethod
    def _get_thumbnail(item_id):
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
