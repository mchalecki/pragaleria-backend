import json


class TestBasic:
    def test_ping(self, client):
        res = client.get('/test/ping')
        assert res.status_code == 200
        assert res.json == {'ping': 'pong'}


class TestTerms:
    def test_if_the_number_of_terms_in_db_is_over_900(self, client):
        res = client.get('/api/terms/1')
        data = json.loads(res.data.decode('utf-8'))
        assert len(data) < 21
