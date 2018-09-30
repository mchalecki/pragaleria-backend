from app.models import models
from app.resources.api_endpoints.postbase import PostsBaseApi


class Auctions(PostsBaseApi):
    def _query_posts(self):
        return models.Posts.query.filter(
            models.Posts.guid.like('%aukcje-wystawy%')
        ).filter(
            models.Posts.post_name.like('%aukcja%')
        ).order_by(
            models.Posts.post_modified.desc()
        )

    def _build_data_list(self):
        result = []
        for parent in self._query_posts():
            revision = models.Posts.query.filter_by(
                post_parent=parent.id
            ).order_by(models.Posts.post_modified.desc()).first()
            data = revision or parent
            if data.post_title and (data.post_excerpt or data.post_content):
                result.append(self._build_post(parent, revision))

        return result
