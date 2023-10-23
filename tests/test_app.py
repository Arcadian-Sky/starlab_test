import pytest
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase
from app.db_connect import get_db_session, create_db_connection
from app.main import init_routes, create_author, download_file, create_book, create_by_file, read_books, read_authors

@pytest.fixture(scope='function')
async def init():
    await create_db_connection()


class TestEndpoints(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        init_routes(app)
        return app

    async def test_create_author(self):
        data = {
            'name': 'Test Author',
            'second_name': 'Test Second Name'
        }
        response = await self.client.post('/author/create', data=data)
        assert response.status == 200
        data = await response.json()
        assert 'author_id' in data

    async def test_create_book(self):
        data = {
            'name': 'Test Book',
        }
        response = await self.client.post('/book/create', data=data)
        assert response.status == 200
        data = await response.json()
        assert 'book_id' in data

    async def test_read_books(self):
        data = {
            'id': 1,
            'name': 'Test Book',
            'author_id': 1,
            'date_published_start': '2023-01-01',
            'date_published_end': '2023-12-31',
            'genre': 'Test Genre',
        }
        response = await self.client.post('/book/list', json=data)
        assert response.status == 200
        data = await response.json()
        assert 'books' in data

    async def test_read_authors(self):
        response = await self.client.get('/author/list')
        assert response.status == 200
        data = await response.json()
        assert isinstance(data, list)

    async def test_download_file(self):
        response = await self.client.get('/download_file?id=1')
        assert response.status == 200

