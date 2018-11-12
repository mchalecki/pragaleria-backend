import consts

from app.models import models

from . import phpmeta


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
            thumbnail_metadata = models.Postmeta.query.filter_by(
                post_id=thumbnail_id.meta_value,
                meta_key='_wp_attachment_metadata'
            ).first().meta_value

            full_size_url = thumbnail.meta_value

            thumbnail_metadata_decoded = phpmeta._to_dict(thumbnail_metadata)
            thumbnail_url = get_thumbnail_url(thumbnail_metadata_decoded, full_size_url)

            return {
                'image_original': f'{consts.PRAGALERIA_UPLOAD_URL}{full_size_url}',
                'image_thumbnail':  f'{consts.PRAGALERIA_UPLOAD_URL}{thumbnail_url}'
            }

    return {
        'image_original': '',
        'image_thumbnail': ''
    }


def get_thumbnail_url(metadata, full_size_url):
    thumbnail_url = full_size_url
    static_part_of_url = '/'.join(full_size_url.split('/')[:2]) + '/'

    if b'sizes' in metadata.keys():
        sizes = metadata[b'sizes']
        if b'thumbnail' in sizes.keys():
            thumbnail = sizes[b'thumbnail']
            if b'file' in thumbnail.keys():
                _file = thumbnail[b'file']
                if _file:
                    thumbnail_url = static_part_of_url + _file.decode()

    return thumbnail_url
