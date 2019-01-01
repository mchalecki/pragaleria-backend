from datetime import datetime
from flask_restful import Resource

import consts
from . import thumbnails, postmeta, html_utils


class BasePostApi(Resource):
    def get(self):
        return sorted(
            self._build_data_list(),
            key=lambda auction: datetime.strptime(
                auction['auction_end'], consts.DATE_FORMAT
            ), reverse=True
        )

    @staticmethod
    def _build_data_list():
        raise NotImplementedError

    @staticmethod
    def _query_posts():
        raise NotImplementedError

    @staticmethod
    def _build_post(parent, revision):
        parent_id = getattr(parent, 'id', '')
        if parent_id:
            data = revision or parent
            auction_start = postmeta.by_key(parent.id, 'aukcja_start', None)
            auction_end = postmeta.by_key(parent.id, 'aukcja_end', None)

            if auction_start and auction_end:
                description = html_utils.clean(getattr(data, 'post_excerpt', ''), True)
                description_excerpt, urls = description if description else (None, None)
                return {
                    'id': parent_id,
                    'title': html_utils.clean(getattr(data, 'post_title', '')),
                    'description_content': html_utils.clean(getattr(data, 'post_content', '')),
                    'urls': urls,
                    'description_excerpt': description_excerpt,
                    'guid': f'{consts.PRAGALERIA_AUCTIONS_URL}{parent.post_name}',
                    'date': str(getattr(data, 'post_modified', '')),
                    'is_current': BasePostApi.is_post_in_the_past(auction_end),
                    'auction_start': auction_start,
                    'auction_end': auction_end,
                    **thumbnails.by_id(parent_id)
                }

    @staticmethod
    def is_post_in_the_past(date_string):
        auction_start_datetime = datetime.strptime(date_string, consts.DATE_FORMAT)
        return auction_start_datetime > datetime.now()
