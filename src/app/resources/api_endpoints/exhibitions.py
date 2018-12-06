from sqlalchemy import not_

from app.models import models
from app.api_utils import base_post_api


class Exhibitions(base_post_api.BasePostApi):
    def _build_data_list(self):
        result = []
        for parent in self._query_posts():
            if parent.post_title:
                post = self._build_post(parent, parent)
                post and result.append(post)

        return result

    def _query_posts(self):
        return models.Posts.query.filter(
            models.Posts.guid.like('%aukcje-wystawy%'),
            models.Posts.post_status == 'publish',
            not_(models.Posts.post_name.like('%aukcja%'))
        ).order_by(models.Posts.post_modified.desc())