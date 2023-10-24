from aiohttp import web
from app.views import *


def init_routes(app):
    app.router.add_get('/', index)
    app.router.add_post('/book/create', create_book)
    app.router.add_get('/book/download', download_file)
    app.router.add_post('/author/create', create_author)
    app.router.add_post('/book/list', read_books)
    app.router.add_get('/author/list', read_authors)
    app.router.add_post('/create_by_file', create_by_file)

    @web.middleware
    async def handle404(request, handler):
        try:
            return await handler(request)
        except web.HTTPNotFound:
            return web.Response(text="404 Not Found", status=404)

    app.middlewares.append(handle404)
