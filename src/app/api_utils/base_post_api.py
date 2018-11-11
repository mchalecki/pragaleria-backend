import consts

from flask_restful import Resource, abort

from app.models import models
from consts import PRAGALERIA_AUCTIONS_URL

from . import thumbnails, postmeta


class BasePostApi(Resource):
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
        image = thumbnails.by_id(parent.id)
        return {
            'id': parent.id,
            'title': data.post_title,
            'description_content': data.post_content,
            'description_excerpt': data.post_excerpt,
            'guid': f'{consts.PRAGALERIA_AUCTIONS_URL}{parent.post_name}',
            'date': str(data.post_modified),
            'auction_start': postmeta.by_key(parent.id, 'aukcja_start'),
            'auction_end': postmeta.by_key(parent.id, 'aukcja_end'),
            'auction_status': postmeta.by_key(parent.id, 'aukcja_status'),
            'image_original': image['image_original'],
            'image_thumbnail': image['image_thumbnail']
        }