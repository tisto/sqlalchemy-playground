"""basic_association.py

illustrate a many-to-many relationship between an
"Book" and a collection of "Author" objects, associating a rank
with each via an association object called "BookAuthor"

The association object pattern is a form of many-to-many which
associates additional data with each association between parent/child.

The example illustrates an "book", referencing a collection
of "authors", with a particular rank paid associated with each "author".

"""

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    book_authors = relationship(
        "BookAuthor",
        cascade="all, delete-orphan",
        backref='book'
    )

    def __init__(self, title):
        self.title = title


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Author(%s)' % self.name


class BookAuthor(Base):
    __tablename__ = 'bookauthor'

    book_id = Column(
        Integer,
        ForeignKey('book.id'),
        primary_key=True
    )

    author_id = Column(
        Integer,
        ForeignKey('author.id'),
        primary_key=True
    )

    rank = Column(String)

    position = Column(Integer)

    def __init__(self, author, rank=None, position=None):
        self.author = author
        self.rank = rank
        self.position = position

    author = relationship(
        Author,
        lazy='joined',
        order_by="BookAuthor.position",
        collection_class=ordering_list('position')
    )


if __name__ == '__main__':
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)

    session = Session(engine)

    # create two authors
    chomsky = Author('Noam Chomsky')
    miller = Author('George A . Miller')

    # create a book with multiple primary authors
    book = Book('Finite State Languages')
    book.book_authors.append(BookAuthor(miller, 'primary', 2))
    book.book_authors.append(BookAuthor(chomsky, 'primary', 1))

    session.add(book)
    session.commit()

    # query the book, print authors with their rank
    books = session.query(Book).all()
    for book in books:
        print('%s:' % book.title)
        print([
            (book_author.author.name, book_author.rank, book_author.position)
            for book_author in book.book_authors
        ])
