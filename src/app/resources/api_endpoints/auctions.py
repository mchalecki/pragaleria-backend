import time

from flask import current_app

from app.api_utils.base_post_api import BasePostApi
from app.api_utils.caching import cache
from app.configs import current_config
from app.models import models
from app.api_utils import base_post_api


class Auctions(BasePostApi):
    @staticmethod
    def _build_data_list():
        result = Auctions._build_results()
        return result

    @staticmethod
    @cache.cached(timeout=current_config.CACHE_TIMEOUT)
    def _build_results():
        result = []
        for parent in Auctions._query_posts():
            revision = models.Posts.query.filter_by(
                post_parent=parent.id
            ).order_by(models.Posts.post_modified.desc()).first()
            data = revision or parent
            if data.post_title and (data.post_excerpt or data.post_content):
                post = BasePostApi._build_post(parent, revision)
                post and result.append(post)
        return result

    @staticmethod
    def _query_posts():
        return models.Posts.query.filter(
            models.Posts.id != 18907,  # some fake post
            models.Posts.guid.like('%aukcje-wystawy%'),
            models.Posts.post_name.like('%aukcja%')
        ).order_by(
            models.Posts.post_modified.desc()
        ).all()
