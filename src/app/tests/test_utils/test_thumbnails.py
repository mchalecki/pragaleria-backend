from app.api_utils import thumbnails


def test_if_by_id_returns_empty_dict_if_postmeta_does_not_exist(app):
    result = thumbnails.by_id(18954)
    assert result == {
        'image_original': '',
        'image_thumbnail': ''
    }


def test_if_returns_all_image_sizes(app):
    result = thumbnails.by_id(29727)
    assert result == {
        'image_original': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5.jpg',
        'image_thumbnail': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5-150x150.jpg',
        'image_big_thumbnail': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5-421x540.jpg',
        'image_large': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5-798x1024.jpg',
        'image_medium': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5-768x985.jpg',
        'image_medium_thumbnail': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5-234x300.jpg',
    }

def test_if_get_thumbnail_returns_empty_if_no_sizes_in_metadata(app):
    metadata = {
       'width': 1169,
       'height': 1500,
       'file':'2018/06/1529158588942b5.jpg',
    }
    assert thumbnails.get_thumbnail_url(metadata, '2018/06/1529158588942b5.jpg') == {
        'image_original': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5.jpg',
    }


def test_if_get_thumbnail_returns_empty_if_no_thumbnail_size_available(app):
    metadata = {
       'width': 1169,
       'height': 1500,
       'file':'2018/06/1529158588942b5.jpg',
       'sizes': {
           'medium': {},
           'medium_large': {},
        },
    }
    assert thumbnails.get_thumbnail_url(metadata, '2018/06/1529158588942b5.jpg') == {
        'image_original': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5.jpg',
    }


def test_if_get_thumbnail_returns_empty_if_no_file_for_thumbnail(app):
    metadata = {
       'width': 1169,
       'height': 1500,
       'file':'2018/06/1529158588942b5.jpg',
       'sizes': {
           'thumbnail': {
               'width': 150,
               'height': 150,
               'mime-type':'image/jpeg'
            },
           'medium': {},
           'medium_large': {},
        },
    }
    assert thumbnails.get_thumbnail_url(metadata, '2018/06/1529158588942b5.jpg') == {
        'image_original': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5.jpg',
    }

def test_if_get_thumbnail_returns_properly(app):
    metadata = {
       'width': 1169,
       'height': 1500,
       'file':'2018/06/1529158588942b5.jpg',
       'sizes': {
           'thumbnail': {
               'file':'1529158588942b5-150x150.jpg',
               'width': 150,
               'height': 150,
               'mime-type':'image/jpeg'
            },
           'medium': {},
           'medium_large': {},
        },
    }
    assert thumbnails.get_thumbnail_url(metadata, '2018/06/1529158588942b5.jpg') == {
        'image_original': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5.jpg',
        'image_thumbnail': 'http://pragaleria.pl/wp-content/uploads/2018/06/1529158588942b5-150x150.jpg'
    }