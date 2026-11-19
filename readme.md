# YaCut — сервис укорачивания ссылок

Сервис позволяет заменить длинный URL коротким адресом, который удобно копировать и отправлять другим пользователям. При переходе по такой ссылке происходит автоматическое перенаправление на исходную страницу.

Дополнительная функция YaCut — загрузка нескольких файлов на Яндекс Диск с получением короткой ссылки для скачивания каждого из них.

### Технологии

Python, Flask, Flask-SQLAlchemy, SQLite, Flask-WTF, WTForms, aiohttp, asyncio, python-dotenv, HTML, CSS, Bootstrap, pytest, Flake8.

### Установка и запуск

#### Получение исходного кода

Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone https://github.com/juliyasg/async-yacut.git
cd async-yacut
```

#### Подготовка окружения

```bash
python -m venv venv
```

Активация для Windows (Git Bash):

```bash
source venv/Scripts/activate
```

Для Linux / macOS:

```bash
source venv/bin/activate
```

#### Установка необходимых библиотек

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Конфигурация

В корне проекта создайте файл .env со следующими переменными:
```
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///yacut.db
DISK_TOKEN=your_yandex_disk_oauth_token
```

Файл .env содержит конфиденциальные данные и не должен добавляться в Git. В проекте он указан в .gitignore.

#### Создание базы данных

```bash
python -c "from yacut import app, db; app.app_context().push(); db.create_all()"
```

#### Запуск сервера

```bash
python -m flask --app yacut run
```

После запуска сервер будет доступен по адресам:

http://127.0.0.1:5000/
http://127.0.0.1:5000/files

Страница / предназначена для сокращения ссылок, /files — для загрузки файлов на Яндекс Диск.

### REST API

YaCut поддерживает два API-эндпоинта для работы с короткими ссылками.

#### Создание ссылки

POST /api/id/

Пример запроса:
```json
{
  "url": "https://www.python.org/",
  "custom_id": "python2026"
}
```

Поле url обязательно. Поле custom_id можно не передавать — в таком случае короткий идентификатор будет сгенерирован автоматически.

Пример ответа (HTTP 201):
```json
{
  "url": "https://www.python.org/",
  "short_link": "http://127.0.0.1:5000/python2026"
}
```

#### Получение исходного адреса

```
GET /api/id/<short_id>/
```

Пример запроса:
```
GET http://127.0.0.1:5000/api/id/python2026/
```

Пример ответа (HTTP 200):
```json
{
  "url": "https://www.python.org/"
}
```

При ошибках API возвращает JSON с полем message и соответствующий HTTP-статус.

Например, если короткий идентификатор отсутствует в базе данных, возвращается ответ со статусом 404.

### Тестирование

Для проверки работы приложения предусмотрены автоматические тесты.

**Запуск тестов из корневой директории проекта:**
```bash
python -m pytest -q
```

**Проверка соответствия Python-кода стилю PEP 8 с помощью Flake8:**
```bash
python -m flake8 yacut config.py constants.py
```

### Автор

[juliyasg](https://github.com/juliyasg)
