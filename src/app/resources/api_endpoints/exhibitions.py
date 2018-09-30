from sqlalchemy import not_

from app.models import models
from app.resources.api_endpoints.postbase import PostsBaseApi


class Exhibitions(PostsBaseApi):
    def _query_posts(self):
        return models.Posts.query.filter(
            models.Posts.guid.like('%/aukcje-wystawy/%'),
            models.Posts.post_status == 'publish'
        ).filter(
            not_(
                models.Posts.post_name.like('%aukcja%')
            )
        ).order_by(models.Posts.post_modified.desc())

    def _build_data_list(self):
        result = []
        for parent in self._query_posts():
            if parent.post_title:
                result.append(self._build_post(parent, parent))

        return result