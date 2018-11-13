import json
from typing import List


def get_endpoint_result(client, endpoint):
    res = client.get(endpoint)
    return json.loads(res.data.decode('utf-8'))


class TestCatalog:
    def test_count(self, client):
        res = client.get('/api/catalog/12179')
        data = json.loads(res.data.decode('utf-8'))
        assert len(data) == 20

    def test_last_entry(self, client):
        res = client.get('/api/catalog/12179')
        data = json.loads(res.data.decode('utf-8'))
        assert data[-1]['title'] == 'Komedia romantyczna'

    def test_404_if_catalog_does_not_exist(self, client):
        res = client.get('/api/catalog/997')
        data = json.loads(res.data.decode('utf-8'))
        assert 'Catalog for this auction does not exist. id: 997' in data['message']

    def test_catalog_field_structure(self, client):
        for auction in get_endpoint_result(client, '/api/auctions'):
            catalog = get_endpoint_result(
                client, '/api/catalog/{}'.format(auction['id'])
            )
            artwork_fields = {
                'id': int,
                'title': str,
                'description': str,
                'initial_price': str,
                'sold_price': str,
                'sold': bool,
                'image_original': str,
                'image_thumbnail': str,
                'author': str,
                'meta': dict,
            }

            for artwork in catalog:
                for key in artwork_fields.keys():
                    assert type(artwork[key]) is artwork_fields[key]
                assert 'dimension' in artwork['meta']
                assert isinstance(artwork['meta']['dimension'], list)
