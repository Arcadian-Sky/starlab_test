import json
import tempfile

from dotenv import load_dotenv
import aiohttp_jinja2
from aiohttp import web
import jinja2
from dbConnect import createdbConnection, getDbSession
from controllers import *

# Загрузка переменных окружения из файла .env
load_dotenv()


@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> object:
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("app/templates"))
    data = await get_data([])
    return data


async def create_author(request: web.Request):
    try:
        data = await request.json()
        name = data.get('name')
        second_name = data.get('second_name')

        db_session = await getDbSession()

        async with db_session as session:
            author_id = await create_new_author(session, name, second_name)
            return web.json_response({'author_id': author_id})

    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)


async def create_book(request: web.Request):
    try:
        data = await request.json()
        name = data.get('name')
        author = data.get('author')
        date_published = data.get('date_published')
        genre = data.get('genre')

        if not all([name, author, date_published, genre]):
            return web.json_response({'error': 'Missing or invalid data in the request'}, status=400)

        db_session = await getDbSession()

        async with db_session as session:
            book_id = await create_new_book(session, name, author, date_published, genre)

            if book_id is not None:
                async with db_session as db_session:
                    query = select(Book).filter(Book.id == book_id)
                    result = await db_session.execute(query)
                    book = result.scalars().first()

                    author = ''
                    if book.author_id:
                        query = select(Author).filter(Author.id == book.author_id)
                        result = await db_session.execute(query)
                        ob_author = result.scalars().first()
                        author = f"{ob_author.name} {' ' + ob_author.second_name if ob_author.second_name else ''}"

                    return web.json_response({
                        'book_id': book.id,
                        'name': book.name,
                        'genre': book.genre,
                        'author_id': book.author_id,
                        'author': author,
                        'date_published': book.date_published.isoformat() if book.date_published else None
                    })
                return web.json_response({'book_id': book_id})
            else:
                return web.json_response({'error': 'Error creating the book'}, status=500)
    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid JSON in the request'}, status=400)


async def create_by_file(request: web.Request):
    try:
        data = await request.post()
        file = data['file']
        print(file)
        if file:
            filename = file.filename
            file_extension = filename.split(".")[-1]

            if file_extension != 'xls' and file_extension != 'xlsx':
                return web.json_response({'error': 'Invalid file format. Please upload a .xls file'}, status=400)

            # file_data = await file.read()

            # Создаем временный файл и сохраняем в него содержимое загруженного файла
            temp_dir = tempfile.mkdtemp()
            temp_file_path = os.path.join(temp_dir, file.filename)

            with open(temp_file_path, 'wb') as f:
                f.write(file.file.read())  # Чтение и запись содержимого файла

            res = await parse_and_create_book(temp_file_path)
            print(res)

            return web.json_response({'message': 'File uploaded and processed successfully'})

    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)


async def read_books(request: web.Request):
    data = await request.json()
    id = data.get('id')
    name = data.get('name')
    author_id = data.get('author_id')
    date_published_start = data.get('date_published_start')
    date_published_end = data.get('date_published_end')
    genre = data.get('genre')

    filters = []
    if name:
        filters.append(Book.name.like(f"%{name}%"))
    if genre:
        filters.append(Book.genre.like(f"%{genre}%"))
    if author_id:
        filters.append(Book.author_id == author_id)
    if id:
        filters.append(Book.id == id)

    if date_published_start:
        from datetime import datetime
        start_date = datetime.strptime(date_published_start, '%Y-%m-%d').date()
        filters.append(Book.date_published >= start_date)

    if date_published_end:
        from datetime import datetime
        end_date = datetime.strptime(date_published_end, '%Y-%m-%d').date()
        filters.append(Book.date_published <= end_date)

    data = await get_data(filters)
    return web.json_response(data['books'])

async def read_authors(request: web.Request):
    db_session = await getDbSession()

    query_authors = select(Author)
    result_authors = await db_session.execute(query_authors)
    authors = result_authors.scalars().all()

    serialized_authors = [{
        'id': author.id,
        'name': author.name,
        'second_name': author.second_name,
    } for author in authors]

    return web.json_response(serialized_authors)

async def on_startup(app):
    await createdbConnection()


def init_routes(app):
    app.router.add_get('/', index)
    app.router.add_post('/book/create', create_book)
    app.router.add_post('/author/create', create_author)
    app.router.add_post('/book/list', read_books)
    app.router.add_get('/author/list', read_authors)
    app.router.add_post('/create_by_file', create_by_file)

    # app.router.add_get('/books/{id}', getBook)

    @web.middleware
    async def handle404(request, handler):
        try:
            return await handler(request)
        except web.HTTPNotFound:
            return web.Response(text="404 Not Found", status=404)

    app.middlewares.append(handle404)


if __name__ == "__main__":
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("app/templates"))

    app.on_startup.append(on_startup)

    init_routes(app)

    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("APP_PORT", 8080)))
