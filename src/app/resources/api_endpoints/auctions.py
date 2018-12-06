from app.models import models
from app.api_utils import base_post_api


class Auctions(base_post_api.BasePostApi):
    def _build_data_list(self):
        result = []
        for parent in self._query_posts():
            revision = models.Posts.query.filter_by(
                post_parent=parent.id
            ).order_by(models.Posts.post_modified.desc()).first()
            data = revision or parent
            if data.post_title and (data.post_excerpt or data.post_content):
                post = self._build_post(parent, revision)
                post and result.append(post)

        return result

    def _query_posts(self):
        return models.Posts.query.filter(
            models.Posts.id != 18907,  # some fake post
            models.Posts.guid.like('%aukcje-wystawy%'),
            models.Posts.post_name.like('%aukcja%')
        ).order_by(
            models.Posts.post_modified.desc()
        )
