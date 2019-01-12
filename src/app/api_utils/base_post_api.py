from datetime import datetime, timedelta

from flask import current_app, request
from flask_restful import Resource
from dateutil.relativedelta import relativedelta

from app.api_utils.caching import cache
from app.configs import current_config
import consts
from . import thumbnails, postmeta, html_utils

PERIOD_TYPES = {
    0: None,
    1: relativedelta(months=1),
    2: relativedelta(months=3),
    3: relativedelta(months=6),
    4: relativedelta(years=1)
}


class BasePostApi(Resource):
    def get(self):
        try:
            period = int(request.args.get('period', 0))
        except ValueError as _:
            current_app.logger.error("Wrong period passed.")
            period = 0
        return self._get_cached(period)

    @classmethod
    def _get_cached(cls, period):
        # currently not cache requires each method to be cachable because in the end methods with self cannot be.
        # TODO implement https://stackoverflow.com/questions/42721927/flask-cache-memoize-not-working-with-flask-restful-resources/42808800#42808800
        result = cls._build_data_list()
        filtered = BasePostApi._filter_by_date(result, period)
        sort = BasePostApi._sort_by_date(data_list=filtered)
        return sort

    @staticmethod
    @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _sort_by_date(data_list):
        return sorted(
            data_list,
            key=lambda auction: datetime.strptime(
                auction['auction_end'], consts.DATE_FORMAT
            ), reverse=True
        )

    @staticmethod
    @cache.memoize(timeout=current_config.CACHE_TIMEOUT)
    def _filter_by_date(data_list, period):
        """
        Filters based on date of evenrt and enum condition passed as argument
        :param data_list: Events to sort
        :param period: One of enum defined in PERIOD_TYPES
        :return: Filtered data_list
        """
        period = PERIOD_TYPES.get(period, None)
        if period:
            now = datetime.now()
            return [i for i in data_list if datetime.strptime(i['auction_end'], consts.DATE_FORMAT) + period > now]
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
