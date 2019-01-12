from app.api_utils.base_post_api import BasePostApi
from app.api_utils.caching import cache
from app.configs import current_config
from app.models import models


class Auctions(BasePostApi):
    @staticmethod
    @cache.cached(timeout=current_config.CACHE_TIMEOUT)
    def _build_data_list():
        result = []
        for parent in Auctions._query_posts():
            revision = models.Posts.query.filter_by(
                post_parent=parent.id
            ).order_by(models.Posts.post_modified.desc()).first()
            if revision and not revision.post_title.isdigit():
                data = revision
            else:
                data = parent
            if data.post_title and (data.post_excerpt or data.post_content):
                post = BasePostApi._build_post(parent, revision)
                post and result.append(post)
        return result

    @staticmethod
    def _query_posts():
        term_relationships_ids = [
            _.object_id for _ in
            models.TermRelationships.query.filter_by(
                term_taxonomy_id='437' # aukcje
            ).all()
        ]

        return models.Posts.query.filter(
            models.Posts.id.in_(term_relationships_ids)
        ).order_by(
            models.Posts.post_modified.desc()
        ).all()
