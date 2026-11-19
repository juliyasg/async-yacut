import asyncio
from urllib.parse import unquote
from uuid import uuid4

import aiohttp
from flask import current_app

from constants import DOWNLOAD_URL, UPLOAD_URL


async def upload_file(session, filename, file_data):
    headers = {
        'Authorization': f'OAuth {current_app.config["DISK_TOKEN"]}'
    }

    disk_path = 'app:/' + f'{uuid4().hex}_{filename}'

    async with session.get(
        UPLOAD_URL,
        headers=headers,
        params={'path': disk_path}
    ) as response:
        response.raise_for_status()

        upload_url = (await response.json())['href']

    async with session.put(upload_url, data=file_data) as response:
        response.raise_for_status()
        location = response.headers['Location']

    file_path = unquote(location).removeprefix('/disk')

    async with session.get(
        DOWNLOAD_URL,
        headers=headers,
        params={'path': file_path}
    ) as response:
        response.raise_for_status()
        await response.json()

    return filename, file_path


async def upload_files(files):
    async with aiohttp.ClientSession() as session:
        tasks = [
            upload_file(session, filename, file_data)
            for filename, file_data in files
        ]
        return await asyncio.gather(*tasks)


async def get_download_link(file_path):
    headers = {
        'Authorization': f'OAuth {current_app.config["DISK_TOKEN"]}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
            DOWNLOAD_URL,
            headers=headers,
            params={'path': file_path}
        ) as response:
            response.raise_for_status()
            return (await response.json())['href']
