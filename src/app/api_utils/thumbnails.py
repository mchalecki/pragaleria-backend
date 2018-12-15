import consts

from . import phpmeta
from . import postmeta


def by_id(item_id):
    thumbnail_id = postmeta.by_key(item_id, '_thumbnail_id', '')
    full_size_url = postmeta.by_key(thumbnail_id, '_wp_attached_file', '')
    thumbnail_metadata = postmeta.by_key(thumbnail_id, '_wp_attachment_metadata')

    if full_size_url and thumbnail_metadata:
        thumbnail_metadata_decoded = phpmeta.to_dict(thumbnail_metadata)
        return get_thumbnail_url(thumbnail_metadata_decoded, full_size_url)
    return {
        'image_original': full_size_url,
        'image_thumbnail': ''
    }


def get_thumbnail_url(metadata, full_size_url):
    result = {
        'image_original': consts.PRAGALERIA_UPLOAD_URL + full_size_url
    }
    if 'sizes' in metadata.keys():
        sizes = metadata['sizes']
        static_part_of_url = '/'.join(full_size_url.split('/')[:2]) + '/'

        def get_thumbnail(key):
            thumbnail = sizes.get(key, '')
            if thumbnail and 'file' in thumbnail.keys():
                _file = thumbnail['file']
                if _file:
                    return consts.PRAGALERIA_UPLOAD_URL + static_part_of_url + _file

        thumbnails = {
            'image_thumbnail': get_thumbnail('thumbnail'),
            'image_medium_thumbnail': get_thumbnail('medium'),
            'image_big_thumbnail': get_thumbnail('big-thumb'),
            'image_medium': get_thumbnail('medium_large'),
            'image_large': get_thumbnail('large'),
        }
        thumbnails = {k: v for k, v in thumbnails.items() if v is not None}
        result = {**result, **thumbnails}
    return result
