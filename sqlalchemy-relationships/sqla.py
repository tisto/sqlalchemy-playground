from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

Base = declarative_base()


class Parent(Base):

    __tablename__ = 'parent'

    id = Column(Integer, primary_key=True)

    name = Column('name', Unicode(255))

    child = relationship("Child", uselist=False, backref="parent")


class Child(Base):

    __tablename__ = 'child'

    id = Column(Integer, primary_key=True)

    name = Column('name', Unicode(255))

    parent_id = Column(Integer, ForeignKey('parent.id'))


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session(engine)

    # create an book with a single author
    jane = Child()
    jane.id = 1
    jane.name = u'Jane'
    john = Parent()
    john.id = 1
    john.name = u'John'
    john.child = jane

    session.add(john)
    session.commit()

    result = session.query(Parent).one()
    print('Parent: {}'.format(result.name))
    print('Child: {}'.format(result.child.name))
