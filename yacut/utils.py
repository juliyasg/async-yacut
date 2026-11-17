import random
import string

from yacut.models import URLMap


SHORT_ID_LENGTH = 6
ALLOWED_SYMBOLS = string.ascii_letters + string.digits


def get_unique_short_id(length=SHORT_ID_LENGTH):
    while True:
        short_id = ''.join(
            random.choices(ALLOWED_SYMBOLS, k=length)
        )
        if short_id == 'files':
            continue
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id
