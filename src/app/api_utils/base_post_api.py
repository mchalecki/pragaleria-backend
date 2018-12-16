from datetime import datetime

from flask import request
from flask_restful import Resource

import consts
from . import thumbnails, postmeta, html_utils


class BasePostApi(Resource):
    def get(self):
        result = self._build_data_list()
        past = request.args.get('past', False) == 'true'
        future = request.args.get('future', False) == 'true'
        if past or future:
            return BasePostApi.filter_by_date_results(result, "auction_start", past)
        return result

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
                return {
                    'id': parent_id,
                    'title': html_utils.clean(getattr(data, 'post_title', '')),
                    'description_content': html_utils.clean(getattr(data, 'post_content', '')),
                    'description_excerpt': html_utils.clean(getattr(data, 'post_excerpt', '')),
                    'guid': f'{consts.PRAGALERIA_AUCTIONS_URL}{parent.post_name}',
                    'date': str(getattr(data, 'post_modified', '')),
                    'auction_start': auction_start,
                    'auction_end': auction_end,
                    'auction_status': bool(int(postmeta.by_key(parent.id, 'aukcja_status', '0'))),
                    **thumbnails.by_id(parent_id)
                }

    @staticmethod
    def filter_by_date_results(result, key, past):
        filtered_results = []
        for i in result:
            auction_start_datetime = datetime.strptime(i[key], "%Y/%m/%d %H:%M")
            is_past = auction_start_datetime < datetime.now()
            if (past and is_past) or (not past and not is_past):
                filtered_results.append(i)
        return filtered_results
