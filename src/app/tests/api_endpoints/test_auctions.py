import json

from app.models import models
from app.api_utils import thumbnails, postmeta, html_utils


def test_all_auctions_satisfy_same_structure(client):
    res = client.get('/api/auctions')
    data = json.loads(res.data.decode('utf-8'))

    auction_fields = {
        'id': int,
        'description_content': str,
        'guid': str,
        'auction_start': str,
        'auction_end': str,
        'is_current': bool,
        'urls': dict,
        'image_thumbnail': str,
    }

    for auction in data:
        for auction_key in auction_fields.keys():
            assert type(auction[auction_key]) is auction_fields[auction_key]


def test_content_of_an_auction_object(client):
    res = client.get('/api/auctions')
    data_list = json.loads(res.data.decode('utf-8'))
    for data in data_list:
        if data['id'] == 16123:
            assert len(data['description_content']) > 1000
            assert data['guid'] == 'http://pragaleria.pl/aukcje-wystawy/9-aukcja-sztuka-aktualna-7-marca-2017-r-godz-19-30'
            assert data['auction_start'] == '2017/03/07 19:30'
            assert data['auction_end'] == '2017/03/07 21:30'
            assert data['is_current'] == False
            assert data['image_original'] == 'http://pragaleria.pl/wp-content/uploads/2017/03/pragaleriabaner-1.jpg'


def test_if_when_there_exists_newer_revision_then_it_is_returned_instead(client):
    auction_test_id = 16123

    res = client.get('/api/auctions')
    data = json.loads(res.data.decode('utf-8'))

    auction_obj = None

    for obj in data:
        if obj['id'] == auction_test_id:
            auction_obj = obj
            break

    assert auction_obj

    real_parent = models.Posts.query.filter_by(id=auction_test_id).first()

    assert real_parent

    new_revision = models.Posts.query.filter_by(
        post_parent=real_parent.id
    ).order_by(models.Posts.post_modified.desc()).first()

    assert new_revision

    assert auction_obj['id'] == real_parent.id
    assert auction_obj['title'] == new_revision.post_title
    assert auction_obj['description_content'] == html_utils.clean(new_revision.post_content)
    assert auction_obj['description_excerpt'] == html_utils.clean(new_revision.post_excerpt)
    assert real_parent.post_name in auction_obj['guid']
    assert auction_obj['auction_start'] == postmeta.by_key(real_parent.id, 'aukcja_start')
    assert auction_obj['auction_end'] == postmeta.by_key(real_parent.id, 'aukcja_end')
    assert auction_obj['image_thumbnail'] == thumbnails.by_id(real_parent.id)['image_thumbnail']


def test_if_when_there_are_no_newer_revisions_then_original_post_is_returned(client):
    auction_test_id = 19819

    res = client.get('/api/auctions')
    data = json.loads(res.data.decode('utf-8'))

    auction_obj = None

    for obj in data:
        if obj['id'] == auction_test_id:
            auction_obj = obj
            break

    assert auction_obj

    real_auction_obj = models.Posts.query.filter_by(id=auction_test_id).first()

    assert real_auction_obj

    assert auction_obj['id'] == real_auction_obj.id
    assert auction_obj['title'] == real_auction_obj.post_title
    assert auction_obj['description_content'] == html_utils.clean(real_auction_obj.post_content)
    assert auction_obj['description_excerpt'] == html_utils.clean(real_auction_obj.post_excerpt)
    assert real_auction_obj.post_name in auction_obj['guid']
    assert auction_obj['auction_start'] == postmeta.by_key(real_auction_obj.id, 'aukcja_start')
    assert auction_obj['auction_end'] == postmeta.by_key(real_auction_obj.id, 'aukcja_end')
