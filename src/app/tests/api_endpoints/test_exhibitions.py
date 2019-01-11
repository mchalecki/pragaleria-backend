import json

from app.models import models
from app.api_utils import thumbnails, postmeta


def test_all_auctions_satisfy_same_structure(client):
    res = client.get('/api/exhibitions')
    data = json.loads(res.data.decode('utf-8'))

    auction_fields = {
        'id': int,
        'description_content': str,
        'guid': str,
        'auction_start': str,
        'auction_end': str,
        'is_current': bool,
        'image_thumbnail': str,
    }

    for auction in data:
        for auction_key in auction_fields.keys():
            assert type(auction[auction_key]) is auction_fields[auction_key]


def test_if_the_original_post_and_not_revision_is_always_returned(client):
    def _perform_realness_test(auction_obj):
        real_auction_obj = models.Posts.query.filter_by(id=auction_obj.id).first()
        assert auction_obj['id'] == real_auction_obj.id
        assert auction_obj['title'] == real_auction_obj.post_title
        assert auction_obj['description_content'] == real_auction_obj.post_content
        assert auction_obj['description_excerpt'] == real_auction_obj.post_excerpt
        assert real_auction_obj.post_name in auction_obj['guid']
        assert auction_obj['auction_start'] == postmeta.by_key(real_auction_obj.id, 'aukcja_start')
        assert auction_obj['auction_end'] == postmeta.by_key(real_auction_obj.id, 'aukcja_end')

    res = client.get('/api/exhibitions')
    data = json.loads(res.data.decode('utf-8'))

    map(_perform_realness_test, data)
