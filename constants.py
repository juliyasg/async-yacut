import string


ORIGINAL_URL_LENGTH = 2048
MAX_SHORT_ID_LENGTH = 16
SHORT_ID_LENGTH = 6
SHORT_ID_ATTEMPTS = 100

ALLOWED_SYMBOLS = string.ascii_letters + string.digits
SHORT_ID_PATTERN = r'^[A-Za-z0-9]+$'

RESERVED_SHORT_IDS = ('files',)

API_HOST = 'https://cloud-api.yandex.net/v1/disk'
UPLOAD_URL = f'{API_HOST}/resources/upload'
DOWNLOAD_URL = f'{API_HOST}/resources/download'
