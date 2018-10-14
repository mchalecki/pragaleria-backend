import phpserialize as php


def to_dict(php_object):
    if php_object:
        return php.loads(php.loads(php_object.encode(), object_hook=php.phpobject))
    
    return {}