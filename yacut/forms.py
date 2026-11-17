from flask_wtf.file import FileRequired
from wtforms import MultipleFileField

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, URL
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректный URL')
        ]
    )

    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=16, message='Не более 16 символов'),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Допустимы только латинские буквы и цифры'
            )
        ]
    )

    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[
            FileRequired(message='Выберите хотя бы один файл')
        ]
    )

    submit = SubmitField('Загрузить')
