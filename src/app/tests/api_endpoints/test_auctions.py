import json

from app.models import models
from app.resources.api_endpoints import auctions
from app.api_utils import thumbnails, postmeta


def test_all_auctions_satisfy_same_structure(client):
    res = client.get('/api/auctions')
    data = json.loads(res.data.decode('utf-8'))
    
    obligatory_fields = [
        'id', 'description_content', 'guid',
        'date', 'auction_start', 'auction_end',
        'auction_status', 'image_thumbnail'
    ]
    assert all(
        key in obj.keys()
        for key in obligatory_fields
        for obj in data
    )

 
def test_structure_of_an_auction_object(client):
    res = client.get('/api/auctions')
    data = json.loads(res.data.decode('utf-8'))[-1]
    
    assert data['id'] == 17355
    assert len(data['description_content']) > 1000
    assert data['guid'] == 'http://pragaleria.pl/aukcje-wystawy/11-aukcja-sztuka-mloda-25-kwietnia-2017-r-godz-19-30'
    assert data['date'] == '2017-06-09 23:03:13'
    assert data['auction_start'] == '2017/04/18 18:45'
    assert data['auction_end'] == '2017/04/25 19:30'
    assert data['auction_status'] == '1'
    assert data['image_original'] == 'http://pragaleria.pl/wp-content/uploads/2017/04/03_Owca-XL-no11-model-Zebrowca-2.jpg'


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
    assert auction_obj['description_content'] == new_revision.post_content
    assert auction_obj['description_excerpt'] == new_revision.post_excerpt
    assert real_parent.post_name in auction_obj['guid']
    assert auction_obj['date'] == str(new_revision.post_modified)
    assert auction_obj['auction_start'] == postmeta.by_key(real_parent.id, 'aukcja_start')
    assert auction_obj['auction_end'] == postmeta.by_key(real_parent.id, 'aukcja_end')
    assert auction_obj['auction_status'] == postmeta.by_key(real_parent.id, 'aukcja_status')
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
    assert auction_obj['description_content'] == real_auction_obj.post_content
    assert auction_obj['description_excerpt'] == real_auction_obj.post_excerpt
    assert real_auction_obj.post_name in auction_obj['guid']
    assert auction_obj['date'] == str(real_auction_obj.post_modified)
    assert auction_obj['auction_start'] == postmeta.by_key(real_auction_obj.id, 'aukcja_start')
    assert auction_obj['auction_end'] == postmeta.by_key(real_auction_obj.id, 'aukcja_end')
    assert auction_obj['auction_status'] == postmeta.by_key(real_auction_obj.id, 'aukcja_status')
    assert auction_obj['image_thumbnail'] == thumbnails.by_id(real_auction_obj.id)['image_thumbnail']
