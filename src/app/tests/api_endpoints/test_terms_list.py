import json


def test_if_for_requested_page_size_all_pages_will_have_this_size_and_pagination_ends(client):
    author_fields = {
        'id': int,
        'name': str,
        'slug': str,
        'image_thumbnail': str,
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
