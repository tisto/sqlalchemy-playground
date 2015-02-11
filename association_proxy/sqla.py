from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    # proxy to 'user_keywords', instantiating UserKeyword
    # assigning the new key to 'special_key', values to
    # 'keyword'.
    keywords = association_proxy(
        'user_keywords',
        'keyword',
        creator=lambda k, v: UserKeyword(special_key=k, keyword=v)
    )

    def __init__(self, name):
        self.name = name


class UserKeyword(Base):
    __tablename__ = 'user_keyword'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keyword.id'), primary_key=True)
    special_key = Column(String)

    # bidirectional user/user_keywords relationships, mapping
    # user_keywords with a dictionary against "special_key" as key.
    user = relationship(
        User,
        backref=backref(
            "user_keywords",
            collection_class=attribute_mapped_collection("special_key"),
            cascade="all, delete-orphan"
            )
        )

    keyword = relationship("Keyword")


class Keyword(Base):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key=True)
    keyword = Column('keyword', String(64))

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return 'Keyword(%s)' % repr(self.keyword)
