from datetime import date
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, Date, ForeignKey


class Author(SQLModel, table=True):
    __tablename__ = 'author'
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(sa_column=Column(String, index=True))
    second_name: str = Field(sa_column=Column(String))


class Book(SQLModel, table=True):
    __tablename__ = 'book'
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(sa_column=Column(String, index=True))
    author_id: int = Field(sa_column=Column(Integer, ForeignKey("author.id")))
    date_published: date = Field(sa_column=Column(Date))
    genre: str = Field(sa_column=Column(String))
    file_path: str = Field(sa_column=Column(String))


