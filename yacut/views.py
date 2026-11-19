import asyncio
from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from constants import RESERVED_SHORT_IDS
from yacut import app, db
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.yandex_disk import get_download_link, upload_files


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    short_url = None

    if form.validate_on_submit():
        custom_id = form.custom_id.data

        if (
            custom_id in RESERVED_SHORT_IDS
            or (
                custom_id
                and URLMap.get_by_short(custom_id) is not None
            )
        ):
            flash(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        else:
            short_id = custom_id or URLMap.get_unique_short_id()

            url_map = URLMap(
                original=form.original_link.data,
                short=short_id
            )
            db.session.add(url_map)
            db.session.commit()

            short_url = url_for(
                'redirect_view',
                short_id=short_id,
                _external=True
            )

    return render_template(
        'index.html',
        form=form,
        short_url=short_url
    )


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.get_by_short(short_id)

    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)

    if url_map.original.startswith('disk:'):
        file_path = url_map.original.removeprefix('disk:')
        download_url = asyncio.run(get_download_link(file_path))
        return redirect(download_url)

    return redirect(url_map.original)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FileUploadForm()
    uploaded_files = []

    if form.validate_on_submit():
        files = [
            (file.filename, file.read())
            for file in form.files.data
            if file.filename
        ]

        if files:
            results = asyncio.run(upload_files(files))

            for filename, file_path in results:
                short_id = URLMap.get_unique_short_id()

                url_map = URLMap(
                    original='disk:' + file_path,
                    short=short_id
                )
                db.session.add(url_map)

                uploaded_files.append({
                    'name': filename,
                    'short_link': url_for(
                        'redirect_view',
                        short_id=short_id,
                        _external=True
                    )
                })

            db.session.commit()

    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files
    )
