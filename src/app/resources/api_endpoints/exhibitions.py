from sqlalchemy import not_

from app.api_utils.base_post_api import BasePostApi
from app.models import models
from app.api_utils import base_post_api


class Exhibitions(BasePostApi):
    @staticmethod
    def _build_data_list():
        result = []
        for parent in Exhibitions._query_posts():
            if parent.post_title:
                post = BasePostApi._build_post(parent, parent)
                post and result.append(post)

        return result

    @staticmethod
    def _query_posts():
        return models.Posts.query.filter(
            models.Posts.guid.like('%aukcje-wystawy%'),
            models.Posts.post_status == 'publish',
            not_(models.Posts.post_name.like('%aukcja%'))
        ).order_by(models.Posts.post_modified.desc())
