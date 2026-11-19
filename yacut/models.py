import random
from datetime import datetime, timezone

from flask import url_for

from constants import (
    ALLOWED_SYMBOLS,
    MAX_SHORT_ID_LENGTH,
    ORIGINAL_URL_LENGTH,
    RESERVED_SHORT_IDS,
    SHORT_ID_ATTEMPTS,
    SHORT_ID_LENGTH,
)
from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(ORIGINAL_URL_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(MAX_SHORT_ID_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    @classmethod
    def get_by_short(cls, short_id):
        return cls.query.filter_by(short=short_id).first()

    @classmethod
    def get_unique_short_id(cls, length=SHORT_ID_LENGTH):
        for _ in range(SHORT_ID_ATTEMPTS):
            short_id = ''.join(
                random.choices(ALLOWED_SYMBOLS, k=length)
            )

            if (
                short_id not in RESERVED_SHORT_IDS
                and cls.get_by_short(short_id) is None
            ):
                return short_id

        raise RuntimeError(
            'Не удалось сгенерировать уникальный идентификатор'
        )

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': url_for(
                'redirect_view',
                short_id=self.short,
                _external=True
            )
        }
