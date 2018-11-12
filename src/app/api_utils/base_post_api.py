import consts

from flask_restful import Resource, abort

from app.models import models
from consts import PRAGALERIA_AUCTIONS_URL

from . import thumbnails, postmeta


class BasePostApi(Resource):
    def get(self):
        return self._build_data_list()

    def _build_data_list(self):
        raise NotImplementedError

    def _query_posts(self):
        raise NotImplementedError

    def _build_post(self, parent, revision):
        parent_id = getattr(parent, 'id', '')
        if parent_id:
            data = revision or parent
            image = thumbnails.by_id(parent_id)
            return {
                'id': parent_id,
                'title': getattr(data, 'post_title', ''),
                'description_content': getattr(data, 'post_content', ''),
                'description_excerpt': getattr(data, 'post_excerpt', ''),
                'guid': f'{consts.PRAGALERIA_AUCTIONS_URL}{parent.post_name}',
                'date': str(getattr(data, 'post_modified', '')),
                'auction_start': postmeta.by_key(parent.id, 'aukcja_start', ''),
                'auction_end': postmeta.by_key(parent.id, 'aukcja_end', ''),
                'auction_status': bool(int(postmeta.by_key(parent.id, 'aukcja_status', '0'))),
                'image_original': image['image_original'],
                'image_thumbnail': image['image_thumbnail']
            }