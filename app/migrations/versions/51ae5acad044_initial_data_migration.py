"""Initial data migration

Revision ID: 51ae5acad044
Revises: cbee4ecb3cde
Create Date: 2023-10-22 19:57:14.774958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from app.models import Book, Author
from sqlalchemy.ext.declarative import declarative_base


# revision identifiers, used by Alembic.
revision: str = '51ae5acad044'
down_revision: Union[str, None] = 'cbee4ecb3cde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


Base = declarative_base()

def upgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    # Создаем автора Agatha Christie
    agatha_christie = Author(name="Agatha", second_name="Christie")
    session.add(agatha_christie)
    session.commit()

    # Получаем ID Agatha Christie
    author_id = agatha_christie.id

    # Добавляем книги с указанием автора
    books = [
        Book(name="Murder on the Orient Express", author_id=author_id, date_published="1934-01-01", genre="Mystery"),
        Book(name="The Murder of Roger Ackroyd", author_id=author_id, date_published="1926-01-01", genre="Mystery"),
        Book(name="And Then There Were None", author_id=author_id, date_published="1939-01-01", genre="Mystery"),
        Book(name="Death on the Nile", author_id=author_id, date_published="1937-01-01", genre="Mystery"),
        Book(name="The ABC Murders", author_id=author_id, date_published="1936-01-01", genre="Mystery"),
        Book(name="Peril at End House", author_id=author_id, date_published="1932-01-01", genre="Mystery")
    ]

    session.add_all(books)
    session.commit()

def downgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    # Удаляем книги Agatha Christie
    author = session.query(Author).filter_by(name="Agatha", second_name="Christie").first()
    if author:
        session.query(Book).filter_by(author_id=author.id).delete()
        session.delete(author)
        session.commit()