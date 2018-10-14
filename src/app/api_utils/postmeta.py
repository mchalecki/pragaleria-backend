from app.models import models


def by_key(post_id, key):
    result = models.Postmeta.query.filter_by(
        post_id=post_id,
        meta_key=key
    ).first()

    if result:
        return result.meta_value
    
    return None
