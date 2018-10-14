import json


class TestCatalog:
    def test_count(self, client):
        res = client.get('/api/catalog/12179')
        data = json.loads(res.data.decode('utf-8'))
        assert len(data) == 20

    def test_last_entry(self, client):
        res = client.get('/api/catalog/12179')
        data = json.loads(res.data.decode('utf-8'))
        assert data[-1]['title'] == 'Komedia romantyczna'
