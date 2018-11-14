import phpserialize as php


def to_dict(php_object_in_decoded_to_string):
    if type(php_object_in_decoded_to_string) is not str:
        print("Not converting, php object must be in string")
        return {}

    php_object_bytes_encoded = php_object_in_decoded_to_string.encode()

    if not php_object_bytes_encoded:
        print("Not converting, failed to encode php object.")
        return {}

    loaded_object = php.loads(php_object_bytes_encoded, object_hook=php.phpobject)

    while type(loaded_object) is bytes:
        loaded_object = php.loads(loaded_object)

    return _convert(loaded_object)


def _convert(data):
    if isinstance(data, bytes):  return data.decode()
    if isinstance(data, dict):   return dict(map(_convert, data.items()))
    if isinstance(data, tuple):  return map(_convert, data)
    return data