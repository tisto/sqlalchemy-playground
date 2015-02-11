from sqla import Base
from sqla import engine
from sqla import User
from sqla import Keyword
import pytest


@pytest.fixture
def sqlite_db():
    pass


def test_create_user():
    Base.metadata.create_all(engine)
    user = User('john')
    user.keywords['sk1'] = Keyword('kw1')
    user.keywords['sk2'] = Keyword('kw2')
    assert [x for x in user.keywords] == ['sk1', 'sk2']
