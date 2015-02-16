from sqla import Base
from sqla import engine
from sqla import Book
from sqla import Author
import pytest


@pytest.fixture
def sqlite_db():
    pass


def test_create_book():
    Base.metadata.create_all(engine)
    book = Book('john')
    book.authors['sk1'] = Author('kw1')
    book.authors['sk2'] = Author('kw2')
    assert [x for x in book.authors] == ['sk1', 'sk2']
