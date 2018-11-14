from app.api_utils import postmeta


def test_by_key_returns_meta_value_if_postmeta_exists(app):
    assert '0' == postmeta.by_key(
        post_id=29727,
        key='aukcja_status',
        default='10'
    )


def test_by_key_returns_default_if_postmeta_not_exists(app):
    assert 'someDefault' == postmeta.by_key(
        post_id=29464,
        key='aukcja_end',
        default='someDefault'
    )
