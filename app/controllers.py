import os
from datetime import datetime

import xlrd
import openpyxl
from sqlalchemy import or_, and_
from sqlmodel import select
from app.dbConnect import getDbSession
from models import *


async def get_data(book_filter: list):
    db_session = await getDbSession()

    query_authors = select(Author)
    result_authors = await db_session.execute(query_authors)
    authors = result_authors.scalars().all()

    serialized_authors = {author.id: {
        'id': author.id,
        'name': author.name,
        'second_name': author.second_name,
    } for author in authors}

    # Выборка по книгам
    query = select(Book)
    if book_filter:
        query = query.filter(and_(*book_filter))

    result = await db_session.execute(query)
    books = result.scalars().all()

    serialized_books = [{
        'id': book.id,
        'name': book.name,
        'genre': book.genre,
        'author': book.author_id,
        'date_published': book.date_published.isoformat() if book.date_published else None
    } for book in books]

    return {
        'books': serialized_books,
        'authors': serialized_authors
    }


async def create_new_author(session: AsyncSession, name: str, second_name: str):
    try:
        new_row = Author(name=name, second_name=second_name)
        async with session.begin():
            session.add(new_row)
        return new_row.id
    except Exception as e:
        print(f"Ошибка при создании автора: {e}")
        return None


async def create_new_book(session: AsyncSession, name: str, author_id: int, date_published: str, genre: str):
    try:
        if date_published:
            date_published = datetime.strptime(date_published, '%Y-%m-%d').date()

        new_book = Book(name=name, author_id=author_id, date_published=date_published, genre=genre)
        async with session.begin():
            session.add(new_book)
        return new_book.id
    except Exception as e:
        print(f"Ошибка при создании книги: {e}")
        return None


async def parse_and_create_book(file_path: str):
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    # sheet = workbook.active

    dbSession = await getDbSession()

    # Парсим авторов
    sheet = workbook.worksheets[1]

    headers = {}
    for row in sheet.iter_rows(min_row=1, max_row=1, values_only=True):
        for idx, cell_value in enumerate(row):
            headers[cell_value] = idx

    # Пройтись по строкам и столбцам для чтения и записи данных
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
        name = row[headers['name']] if 'name' in headers else None
        second_name = row[headers['second_name']] if 'second_name' in headers else None

        async with dbSession as session:
            author_id = await create_new_author(session, name, second_name)

    # Парсим книги
    sheet = workbook.worksheets[0]
    # Парсим заголовки колонок
    headers = {}
    for row in sheet.iter_rows(min_row=1, max_row=1, values_only=True):
        for idx, cell_value in enumerate(row):
            headers[cell_value] = idx

    # Пройтись по строкам и столбцам для чтения и записи данных
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
        name = row[headers['name']] if 'name' in headers else None
        author = row[headers['author']] if 'author' in headers else None
        author_id = row[headers['author_id']] if 'author_id' in headers else None
        date_published = row[headers['date_published']] if 'date_published' in headers else None
        genre = row[headers['genre']] if 'genre' in headers else None

        if author and author_id is None:
            author_id = session.query(Author).filter(or_(Author.name == author, Author.second_name == author)).first()

        async with dbSession as session:
            book_id = await create_new_book(session, name, author_id, date_published, genre)

    workbook.close()

    os.remove(file_path)

    return None
