import consts

from app.models import models

from . import phpmeta
from . import postmeta


def by_id(item_id):
    thumbnail_id = postmeta.by_key(item_id, '_thumbnail_id', '')
    full_size_url = postmeta.by_key(thumbnail_id, '_wp_attached_file')
    thumbnail_metadata = postmeta.by_key(thumbnail_id, '_wp_attachment_metadata')

    if full_size_url and thumbnail_metadata:
        thumbnail_metadata_decoded = phpmeta.to_dict(thumbnail_metadata)
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

    if 'sizes' in metadata.keys():
        sizes = metadata['sizes']
        if 'thumbnail' in sizes.keys():
            thumbnail = sizes['thumbnail']
            if 'file' in thumbnail.keys():
                _file = thumbnail['file']
                if _file:
                    thumbnail_url = static_part_of_url + _file

    return thumbnail_url
