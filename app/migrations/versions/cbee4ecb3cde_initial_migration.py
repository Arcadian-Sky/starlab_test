"""Initial migration

Revision ID: cbee4ecb3cde
Revises: 
Create Date: 2023-10-22 19:04:03.342242

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from alembic import context


# revision identifiers, used by Alembic.
from sqlalchemy.exc import ProgrammingError

revision: str = 'cbee4ecb3cde'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    try:
        if not connection.dialect.has_table(connection, 'author'):
            # Создаем таблицу для модели Author
            op.create_table(
                'author',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('name', sa.String(length=255), nullable=True),
                sa.Column('second_name', sa.String(length=255), nullable=True),
                sa.PrimaryKeyConstraint('id')
            )
    except ProgrammingError:
        pass

    try:
        if not connection.dialect.has_table(connection, 'book'):
            # Создаем таблицу для модели Book
            op.create_table(
                'book',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('name', sa.String(length=255), nullable=True),
                sa.Column('author_id', sa.Integer(), nullable=True),
                sa.Column('date_published', sa.Date(), nullable=True),
                sa.Column('genre', sa.String(length=255), nullable=True),
                sa.Column('file_path', sa.String(length=255), nullable=True),
                sa.PrimaryKeyConstraint('id')
            )
    except ProgrammingError:
        pass





    pass


def downgrade() -> None:
    # Удаляем таблицу для модели Author
    op.drop_table('author')

    # Удаляем таблицу для модели Book
    op.drop_table('book')
    pass
