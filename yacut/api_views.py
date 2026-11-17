import re

from flask import jsonify, request, url_for

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')

    if not custom_id:
        custom_id = get_unique_short_id()
    elif (
        not isinstance(custom_id, str)
        or len(custom_id) > 16
        or not re.fullmatch(r'[A-Za-z0-9]+', custom_id)
    ):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки'
        )

    if custom_id == 'files' or URLMap.query.filter_by(
        short=custom_id
    ).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    url_map = URLMap(
        original=data['url'],
        short=custom_id
    )
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'redirect_view',
            short_id=url_map.short,
            _external=True
        )
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()

    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': url_map.original}), 200
