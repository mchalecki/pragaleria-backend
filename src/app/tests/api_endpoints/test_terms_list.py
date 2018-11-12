import json

from app.models import models
from app.resources.api_endpoints import auctions
from app.api_utils import thumbnails, postmeta


def test_all_terms_satisfy_same_structure(client):
    res = client.get('/api/authors')
    data = json.loads(res.data.decode('utf-8'))

    obligatory_fields = ['id', 'name', 'slug', 'thumbnail']
    assert all(
        key in obj.keys()
        for key in obligatory_fields
        for obj in data
    )


def test_if_for_requested_page_size_all_pages_will_have_this_size_and_pagination_ends(client):
    i = 0

    while True:
        res = client.get(f'/api/authors?page={i}&size=25')
        data = json.loads(res.data.decode('utf-8'))
        i += 1
        if len(data) == 0:
            break

        assert len(data) == 25

    assert True
