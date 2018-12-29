import consts
import datetime

from flask_restful import Resource, abort

from app.models import models
from consts import PRAGALERIA_AUCTIONS_URL, DATE_FORMAT

from . import thumbnails, postmeta, html_utils


class BasePostApi(Resource):
    def get(self):
        return sorted(
            self._build_data_list(),
            key=lambda auction: datetime.datetime.strptime(
                auction['auction_end'], DATE_FORMAT
            ), reverse=True
        )

    def _build_data_list(self):
        raise NotImplementedError

    def _query_posts(self):
        raise NotImplementedError

    def _build_post(self, parent, revision):
        parent_id = getattr(parent, 'id', '')
        if parent_id:
            data = revision or parent
            auction_start = postmeta.by_key(parent.id, 'aukcja_start', None)
            auction_end = postmeta.by_key(parent.id, 'aukcja_end', None)

            if auction_start and auction_end:
                auction_status = datetime.datetime.strptime(
                    auction_end, DATE_FORMAT
                ) > datetime.datetime.now()
                return {
                    'id': parent_id,
                    'title': html_utils.clean(getattr(data, 'post_title', '')),
                    'description_content': html_utils.clean(getattr(data, 'post_content', '')),
                    'description_excerpt': html_utils.clean(getattr(data, 'post_excerpt', '')),
                    'guid': f'{consts.PRAGALERIA_AUCTIONS_URL}{parent.post_name}',
                    'auction_start': auction_start,
                    'auction_end': auction_end,
                    'auction_status': auction_status,
                    **thumbnails.by_id(parent_id)
                }