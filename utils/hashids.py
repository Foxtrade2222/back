import string

from django.conf import settings
from hashids import Hashids

__HASHID = Hashids(
    min_length=settings.MIN_LENGTH,
    alphabet=string.ascii_uppercase + string.digits,
    salt=settings.SALT,
)


def encode_pk(pk: int):
    return __HASHID.encode(pk)


def decode_pk(code: str):
    return __HASHID.decode(code)
