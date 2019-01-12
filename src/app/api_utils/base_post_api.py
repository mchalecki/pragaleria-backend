from datetime import datetime

from flask import current_app, request
from flask_restful import Resource

from app.api_utils.caching import cache
from app.configs import current_config
from consts import PRAGALERIA_AUCTIONS_URL, DATE_FORMAT, PERIOD_FILTER_TYPES, TITLE_FILTER_TYPES
from . import thumbnails, postmeta, html_utils


class BasePostApi(Resource):
    def get(self):
        period_filter_id = BasePostApi.get_enum_id('period')
        title_filter_id = BasePostApi.get_enum_id('category')
        return self._get_cached(period_filter_id, title_filter_id)

    @classmethod
    def _get_cached(cls, period_filter_id, title_filter_id):
        # currently not cache requires each method to be cachable because in the end methods with self cannot be.
        # TODO implement https://stackoverflow.com/questions/42721927/flask-cache-memoize-not-working-with-flask-restful-resources/42808800#42808800
        result = cls._build_data_list()
        result = BasePostApi._sort_by_date(data_list=result)
        result = BasePostApi._filter_by_date(result, period_filter_id)
        result = BasePostApi._filter_by_title(result, title_filter_id)
        return result

    @staticmethod
    @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _sort_by_date(data_list):
        return sorted(
            data_list,
            key=lambda auction: datetime.strptime(
                auction['auction_end'], DATE_FORMAT
            ), reverse=True
        )

    @staticmethod
    @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _filter_by_date(data_list, period_filter_id):
        """
        Filters based on date of evenrt and enum condition passed as argument
        :param data_list: Events to sort
        :param period_filter_id: One of enum defined in PERIOD_TYPES
        :return: Filtered data_list
        """
        period_filter_id = PERIOD_FILTER_TYPES.get(period_filter_id, None)
        if period_filter_id:
            now = datetime.now()
            return [i for i in data_list if datetime.strptime(i['auction_end'], DATE_FORMAT) + period_filter_id > now]
        else:
            return data_list

    @staticmethod
    @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _filter_by_title(data_list, title_filter_id):
        title_filter = TITLE_FILTER_TYPES.get(title_filter_id, None)
        current_app.logger.debug(title_filter_id)
        current_app.logger.debug(title_filter)

        if title_filter:
            return [i for i in data_list if title_filter in i['title']]
        else:
            return data_list

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
                'guid': f'{PRAGALERIA_AUCTIONS_URL}{parent.post_name}',
                **thumbnails.by_id(parent_id)
            }

            auction_info = {
                'auction_end': ':'.join(str(getattr(data, 'post_date', '')).replace('-', '/').split(':')[:-1]),
                'is_current': False,
            }
            auction_info['auction_start'] = auction_info['auction_end']

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
        auction_start_datetime = datetime.strptime(date_string, DATE_FORMAT)
        return auction_start_datetime > datetime.now()

    @staticmethod
    def get_enum_id(key):
        """Receive from get request arguments, try to parse them to ints. Return 0(all) if no argument in request."""
        try:
            val = int(request.args.get(key, 0))
        except ValueError as _:
            current_app.logger.error(f"Wrong {key} passed.")
            val = 0
        return val
