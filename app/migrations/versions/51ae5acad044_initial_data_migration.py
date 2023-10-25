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
    author = Author(name="George", second_name="Orwell")
    session.add(author)
    author = Author(name="Stephen", second_name="King")
    session.add(author)
    author = Author(name="Theodore", second_name="Dreiser")
    session.add(author)
    author = Author(name="George Orwell", second_name="Blair")
    session.add(author)

    # Создаем автора Agatha Christie
    agatha_christie = Author(name="Agatha", second_name="Christie")
    session.add(agatha_christie)
    session.commit()
    author_id = agatha_christie.id

    books = [
        Book(name="Murder on the Orient Express", author_id=author_id, date_published="1934-01-01", genre="Mystery"),
        Book(name="The Murder of Roger Ackroyd", author_id=author_id, date_published="1926-01-01", genre="Mystery"),
        Book(name="And Then There Were None", author_id=author_id, date_published="1939-01-01", genre="Mystery"),
        Book(name="Death on the Nile", author_id=author_id, date_published="1937-01-01", genre="Mystery"),
        Book(name="The ABC Murders", author_id=author_id, date_published="1936-01-01", genre="Mystery"),
        Book(name="Peril at End House", author_id=author_id, date_published="1932-01-01", genre="Mystery"),
        Book(name="The Mysterious Affair at Styles", author_id=author_id, date_published="1920-01-01", genre="Mystery"),
        Book(name="The Secret Adversary", author_id=author_id, date_published="1922-01-01", genre="Mystery"),
        Book(name="The Murder at the Vicarage", author_id=author_id, date_published="1930-01-01", genre="Mystery"),
        Book(name="Five Little Pigs", author_id=author_id, date_published="1942-01-01", genre="Mystery"),
        Book(name="Hercule Poirot's Christmas", author_id=author_id, date_published="1938-01-01", genre="Mystery"),
        Book(name="The Hollow", author_id=author_id, date_published="1946-01-01", genre="Mystery"),
        Book(name="Curtain", author_id=author_id, date_published="1975-01-01", genre="Mystery"),
        Book(name="Appointment with Death", author_id=author_id, date_published="1938-01-01", genre="Mystery"),
        Book(name="Evil Under the Sun", author_id=author_id, date_published="1941-01-01", genre="Mystery"),
        Book(name="Nemesis", author_id=author_id, date_published="1971-01-01", genre="Mystery"),
        Book(name="The Body in the Library", author_id=author_id, date_published="1942-01-01", genre="Mystery"),
        Book(name="The Moving Finger", author_id=author_id, date_published="1942-01-01", genre="Mystery"),
        Book(name="A Caribbean Mystery", author_id=author_id, date_published="1964-01-01", genre="Mystery"),
        Book(name="A Pocket Full of Rye", author_id=author_id, date_published="1953-01-01", genre="Mystery"),
        Book(name="The Pale Horse", author_id=author_id, date_published="1961-01-01", genre="Mystery"),
        Book(name="One, Two, Buckle My Shoe", author_id=author_id, date_published="1940-01-01", genre="Mystery"),
        Book(name="The Mirror Crack'd from Side to Side", author_id=author_id, date_published="1962-01-01", genre="Mystery"),
        Book(name="A Murder Is Announced", author_id=author_id, date_published="1950-01-01", genre="Mystery")
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