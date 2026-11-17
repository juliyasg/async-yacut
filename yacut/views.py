import asyncio

from flask import abort, flash, redirect, render_template, url_for
from yacut.yandex_disk import get_download_link, upload_files

from yacut import app, db
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    short_url = None

    if form.validate_on_submit():
        custom_id = form.custom_id.data

        if custom_id == 'files' or (
            custom_id and URLMap.query.filter_by(
                short=custom_id
            ).first()
        ):
            flash('Предложенный вариант короткой ссылки уже существует.')
        else:
            short_id = custom_id or get_unique_short_id()

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
    url_map = URLMap.query.filter_by(short=short_id).first()

    if url_map is None:
        abort(404)

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
                short_id = get_unique_short_id()

                url_map = URLMap(
                    original=f'disk: {file_path}',
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
