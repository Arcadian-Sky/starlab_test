import json
import jinja2
import tempfile
import mimetypes
import aiohttp_jinja2
from urllib.parse import quote

from aiohttp import web
from dotenv import load_dotenv
from aiohttp.web import FileResponse

from app import *
from app.controllers import *


@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> object:
    # aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("app/templates"))
    data = await get_data([])
    return data


async def create_author(request: web.Request):
    try:
        data = await request.post()
        name = data.get('name')
        second_name = data.get('second_name') if 'second_name' in data else None
        if not all([name]):
            return web.json_response({'error': 'Missing or invalid data in the request'}, status=400)

        async with get_db_session() as db_session:
            author_id = await create_new_author(db_session, name, second_name)
            return web.json_response({'author_id': author_id})

    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)


async def create_book(request: web.Request):
    try:
        data = await request.post()
        name = data['name']
        author = data['author_id'] if 'author_id' in data else None
        date_published = data['date_published'] if 'date_published' in data else None
        genre = data['genre'] if 'genre' in data else None
        file = data['file'] if 'file' in data else None

        if not all([name]):
            return web.json_response({'error': 'Missing or invalid data in the request'}, status=400)

        async with get_db_session() as session:
            book_id = await create_new_book(session, name, author, date_published, genre, file)

            if book_id is not None:
                async with get_db_session() as db_session:
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
                        'file_path': book.file_path,
                        'date_published': book.date_published.isoformat() if book.date_published else None
                    })
            else:
                return web.json_response({'error': 'Error creating the book'}, status=500)
    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid JSON in the request'}, status=400)


async def decline_by_file(request: web.Request):
    try:
        data = await request.post()
        file = data['file']

        if file:
            filename = file.filename
            file_extension = filename.split(".")[-1]

            if file_extension != 'xlsx':
                return web.json_response({'error': 'Invalid file format. Please upload a .xls file'}, status=400)

            # file_data = await file.read()

            # Создаем временный файл и сохраняем в него содержимое загруженного файла
            temp_dir = tempfile.mkdtemp()
            temp_file_path = os.path.join(temp_dir, file.filename)

            with open(temp_file_path, 'wb') as f:
                f.write(file.file.read())  # Чтение и запись содержимого файла

            res = await parse_and_decline_book(temp_file_path)
            return web.json_response({'message': 'File uploaded and processed successfully'})

    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)


async def read_books(request: web.Request):
    data = await request.json()
    id = data.get('id') if 'id' in data else None
    name = data.get('name') if 'name' in data else None
    author_id = data.get('author_id') if 'author_id' in data else None
    date_published_start = data.get('date_published_start') if 'date_published_start' in data else None
    date_published_end = data.get('date_published_end') if 'date_published_end' in data else None
    genre = data.get('genre') if 'genre' in data else None

    filters = []
    if name:
        filters.append(Book.name.like(f"%{name}%"))
    if genre:
        filters.append(Book.genre.like(f"%{genre}%"))
    if author_id:
        filters.append(Book.author_id == author_id)
    if id:
        filters.append(Book.id == int(id))

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
    async with get_db_session() as db_session:
        query_authors = select(Author)
        result_authors = await db_session.execute(query_authors)
        authors = result_authors.scalars().all()

        serialized_authors = [{
            'id': author.id,
            'name': author.name,
            'second_name': author.second_name,
        } for author in authors]

    return web.json_response(serialized_authors)


async def download_file(request):
    id = int(request.query.get('id', default=None))

    if not all([id]):
        return web.json_response({'error': 'Missing or invalid data in the request'}, status=400)

    async with get_db_session() as db_session:
        query = select(Book).filter(Book.id == id)
        result = await db_session.execute(query)
        book = result.scalars().first()
        current_directory = os.path.dirname(os.path.abspath(__file__))

        if book.file_path:
            file_path = os.path.join(current_directory, book.file_path)

            mimetype, _ = mimetypes.guess_type(file_path)

            filename = quote(os.path.basename(file_path))

            if os.path.exists(file_path):
                if mimetype:
                    return FileResponse(file_path, headers={
                        "Content-Type": mimetype,
                        "Content-Disposition": f'attachment; filename="{filename}"'
                    })
                else:
                    return FileResponse(file_path, headers={
                        "Content-Type": "application/octet-stream",
                        "Content-Disposition": f'attachment; filename="{filename}"'
                    })
            else:
                return web.Response(text='File not found', status=404)
        else:
            return web.Response(text='Book has no File', status=404)
