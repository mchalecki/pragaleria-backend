from sqlalchemy import not_

from app.api_utils.base_post_api import BasePostApi
from app.models import models


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
        term_relationships_ids = [
            _.object_id for _ in
            models.TermRelationships.query.filter_by(
                term_taxonomy_id='438' # wystawy
            ).all()
        ]

        return models.Posts.query.filter(
            models.Posts.id.in_(term_relationships_ids)
        ).order_by(
            models.Posts.post_modified.desc()
        ).all()
