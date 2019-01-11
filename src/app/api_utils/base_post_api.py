from datetime import datetime
from flask_restful import Resource

from app.api_utils.caching import cache
from app.configs import current_config
import consts
from . import thumbnails, postmeta, html_utils


class BasePostApi(Resource):
    @cache.cached(timeout=current_config.CACHE_TIMEOUT)
    def get(self):
        return BasePostApi._sorted_by_date(
            data_list=self._build_data_list()
        )

    @staticmethod
    def _sorted_by_date(data_list):
        return sorted(
            data_list,
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
            if revision and not revision.post_title.isdigit():
                data = revision
            else:
                data = parent
            auction_start = postmeta.by_key(parent.id, 'aukcja_start', None)
            auction_end = postmeta.by_key(parent.id, 'aukcja_end', None)

            description = html_utils.clean(getattr(data, 'post_excerpt', ''), True)
            description_excerpt, urls = description if description else (None, None)

            result = {
                'id': parent_id,
                'title': html_utils.clean(getattr(data, 'post_title', '')),
                'description_content': html_utils.clean(getattr(data, 'post_content', '')),
                'urls': urls,
                'description_excerpt': description_excerpt,
                'guid': f'{consts.PRAGALERIA_AUCTIONS_URL}{parent.post_name}',
                **thumbnails.by_id(parent_id)
            }

            auction_info = {
                'auction_end': ':'.join(str(getattr(data, 'post_date', '')).replace('-', '/').split(':')[:-1])
            }
            auction_info['auction_start'] = auction_info['auction_end']
            auction_info['is_current'] = False

            if auction_start or auction_end:
                if auction_end:
                    auction_info['auction_end'] = auction_end
                    auction_info['is_current'] = BasePostApi.is_post_in_the_past(auction_end)
                if auction_start:
                    auction_info['auction_start'] = auction_start

            return {
                **result,
                **auction_info
            }

    @staticmethod
    def is_post_in_the_past(date_string):
        auction_start_datetime = datetime.strptime(date_string, consts.DATE_FORMAT)
        return auction_start_datetime > datetime.now()
