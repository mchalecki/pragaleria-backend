import phpserialize as php


def to_dict(php_object):
    if php_object:
        return php.loads(php.loads(php_object.encode(), object_hook=php.phpobject))

    return {}


def _to_dict(php_object_in_string):
    php_bytes = php_object_in_string.encode()

    if php_bytes:
        return php.loads(php_bytes, object_hook=php.phpobject)

    return {}
