import json


# TODO call api once for class in setup_class
class TestBasic:
    def test_ping(self, client):
        res = client.get('/test/ping')
        assert res.status_code == 200
        assert res.json == {'ping': 'pong'}


class TestTerms:
    def test_count(self, client):
        res = client.get('/api/authors/1/20')
        data = json.loads(res.data.decode('utf-8'))
        assert len(data) < 21

    def test_last_entry(self, client):
        res = client.get('/api/authors/1/20')
        data = json.loads(res.data.decode('utf-8'))
        assert data[-1]['name'] == 'Tomek Wojtysek'


class TestCatalog:
    def test_count(self, client):
        res = client.get('/api/catalog/12179')
        data = json.loads(res.data.decode('utf-8'))
        assert len(data) == 20

    def test_last_entry(self, client):
        res = client.get('/api/catalog/12179')
        data = json.loads(res.data.decode('utf-8'))
        assert data[-1]['title'] == 'Komedia romantyczna'


class TestExhibitions:
    def test_count(self, client):
        res = client.get('/api/exhibitions')
        data = json.loads(res.data.decode('utf-8'))
        assert len(data) == 13

    def test_last_entry(self, client):
        res = client.get('/api/exhibitions')
        data = json.loads(res.data.decode('utf-8'))
        assert data[-1]['title'] == 'KRZY.WE 2'


class TestAuctions:
    def test_catalog_count(self, client):
        res = client.get('/api/auctions')
        data = json.loads(res.data.decode('utf-8'))
        assert len(data) == 20

    def test_last_entry(self, client):
        res = client.get('/api/auctions')
        data = json.loads(res.data.decode('utf-8'))
        assert data[-1]['title'] == '11 Aukcja Sztuka Młoda - 25 kwietnia 2017 r., godz. 19.30'
