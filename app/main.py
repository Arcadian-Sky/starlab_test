import json
import os

import jinja2
import tempfile
import mimetypes
import aiohttp_jinja2
from urllib.parse import quote

from aiohttp import web
from dotenv import load_dotenv
from aiohttp.web import FileResponse
from app.db_connect import create_db_connection, get_db_session
from app.route import init_routes


# Загрузка переменных окружения из файла .env
load_dotenv()


async def on_startup(app):
    await create_db_connection()


if __name__ == "__main__":
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("app/templates"))

    app.on_startup.append(on_startup)

    init_routes(app)

    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("APP_PORT", 8080)))
