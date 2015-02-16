from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    # proxy to 'book_authors', instantiating BookAuthor
    # assigning the new key to 'rank', values to
    # 'author'.
    authors = association_proxy(
        'book_authors',
        'author',
        creator=lambda k, v: BookAuthor(rank=k, author=v)
    )

    def __init__(self, name):
        self.name = name


class BookAuthor(Base):
    __tablename__ = 'book_author'
    book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'), primary_key=True)
    rank = Column(String)

    # bidirectional book/book_authors relationships, mapping
    # book_authors with a dictionary against "rank" as key.
    book = relationship(
        Book,
        backref=backref(
            "book_authors",
            collection_class=attribute_mapped_collection("rank"),
            cascade="all, delete-orphan"
            )
        )

    author = relationship("Author")


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    author = Column('author', String(64))

    def __init__(self, author):
        self.author = author

    def __repr__(self):
        return 'Author(%s)' % repr(self.author)
