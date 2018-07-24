class TestBasic:
    def test_ping(self, client):
        res = client.get('/test/ping')
        assert res.status_code == 200
        assert res.json == {'ping': 'pong'}
