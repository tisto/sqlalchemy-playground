from sqlalchemy import LargeBinary
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

Base = declarative_base()


class Book(Base):

    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)

    title = Column(Unicode(255), nullable=False)

    description = Column(Unicode(255), nullable=False)

    file = Column('file', LargeBinary),

    def __init__(self, title):
        self.title = title


if __name__ == '__main__':
    engine = create_engine('postgresql://test:test@localhost:5432/test')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session(engine)

    # create an book with a single author
    book1 = Book('Syntactic Structures')
    book1.description = 'Syntactic Structures is a book in linguistics by American linguist Noam Chomsky, first published in 1957'  # noqa

    with open('file.pdf', 'rb') as file:
        book1.file = file.read()

    session.add(book1)
    session.commit()

    result = session.query(Book).one()
    print(result.title)
    print(result.description)
    #print(result.file)
