from app.models import models


def by_key(post_id, key, default=None):
    result = models.Postmeta.query.filter_by(
        post_id=post_id,
        meta_key=key
    ).first()

    if result and result.meta_value:
        return result.meta_value

    return default
