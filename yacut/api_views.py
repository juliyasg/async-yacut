import re
from http import HTTPStatus

from flask import jsonify, request

from constants import (
    MAX_SHORT_ID_LENGTH,
    RESERVED_SHORT_IDS,
    SHORT_ID_PATTERN,
)
from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')

    if not custom_id:
        custom_id = URLMap.get_unique_short_id()
    elif (
        not isinstance(custom_id, str)
        or len(custom_id) > MAX_SHORT_ID_LENGTH
        or not re.fullmatch(SHORT_ID_PATTERN, custom_id)
    ):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки'
        )

    if (
        custom_id in RESERVED_SHORT_IDS
        or URLMap.get_by_short(custom_id) is not None
    ):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    url_map = URLMap(
        original=data['url'],
        short=custom_id
    )

    db.session.add(url_map)
    db.session.commit()

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.get_by_short(short_id)

    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND
        )

    return jsonify({'url': url_map.original}), HTTPStatus.OK
