"""Dot that."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(Base):
    """Handle the book entity."""

    __tablename__ = 'BOOK'

    book_id = Column(Integer, primary_key=True, auto_increment=True)
    title = Column(String(length=255))
