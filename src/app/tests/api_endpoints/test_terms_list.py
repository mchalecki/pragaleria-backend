import json


def test_if_for_requested_page_size_all_pages_will_have_this_size_and_pagination_ends(client):
    author_fields = {
        'id': int,
        'name': str,
        'slug': str,
    }

    i = 0

    while True:
        res = client.get(f'/api/authors?page={i}&size=25')
        data = json.loads(res.data.decode('utf-8'))

        for author in data:
            for author_key in author_fields.keys():
                assert type(author[author_key]) is author_fields[author_key]

        i += 1
        if len(data) == 0:
            break

        assert len(data) == 25

    assert True


def test_404_if_invalid_page_or_size(client):
    res = client.get(f'/api/authors?page=pikpik&size=hahaha')
    data = json.loads(res.data.decode('utf-8'))
    assert 'Error querying Terms.' in data['message']


def test_authors_search_query(client):
    res = client.get(f'/api/authors?search=grajek')
    data = json.loads(res.data.decode('utf-8'))
    assert data == [
        {
            'id': 190,
            'name': 'Daria Grajek',
            'slug': 'daria-grajek',
            'image_original': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466354103.jpg',
            'image_thumbnail': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466354103-150x150.jpg',
            'image_medium_thumbnail': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466354103-300x220.jpg',
            'image_big_thumbnail': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466354103-737x540.jpg',
            'image_medium': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466354103-768x563.jpg',
            'image_large': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466354103-1024x750.jpg'
        },
        {
            'id': 11,
            'name': 'Dariusz Grajek',
            'slug': 'dariusz-grajek',
            'image_original': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466351975.jpg',
            'image_thumbnail': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466351975-150x150.jpg',
            'image_medium_thumbnail': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466351975-300x200.jpg',
            'image_big_thumbnail': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466351975-800x533.jpg',
            'image_medium': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466351975-768x512.jpg',
            'image_large': 'http://pragaleria.pl/wp-content/uploads/2017/03/1466351975-1024x683.jpg'
        }
    ]