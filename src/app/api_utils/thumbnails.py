import consts

from app.models import models


def by_id(item_id):
    thumbnail_id = models.Postmeta.query.filter_by(
        post_id=item_id,
        meta_key='_thumbnail_id'
    ).first()

    if thumbnail_id:
        thumbnail = models.Postmeta.query.filter_by(
            post_id=thumbnail_id.meta_value,
            meta_key='_wp_attached_file'
        ).first()

        if thumbnail:
            return f'{consts.PRAGALERIA_UPLOAD_URL}{thumbnail.meta_value}'

    return ''