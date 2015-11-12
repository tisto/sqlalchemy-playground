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

    children = relationship(
        "Child",
        backref="parent",
        cascade="all, delete, delete-orphan"
    )


class Child(Base):

    __tablename__ = 'child'

    id = Column(Integer, primary_key=True)

    name = Column('name', Unicode(255))

    parent_id = Column(Integer, ForeignKey('parent.id'))


if __name__ == '__main__':

    # DB setup
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session(engine)

    # create parent / child relationship
    jane = Child()
    jane.id = 1
    jane.name = u'Jane'
    jone = Child()
    jone.id = 2
    jone.name = u'Jone'
    john = Parent()
    john.id = 1
    john.name = u'John'
    john.children = [jane, jone]

    session.add(john)
    session.commit()

    # query db
    result = session.query(Parent).one()
    print('')
    print('Parent:')
    print('- {}'.format(result.name))
    print('Children:')
    for child in result.children:
        print('- {}'.format(child.name))

    # delete parent
    print('')
    print('Delete John (Children will be deleted automatically)')
    session.delete(john)

    print('# Parents: %s' % session.query(Parent).count())
    print('# Children: %s' % session.query(Child).count())

    print('')
    print('Bulk Create 100 Parents with 200 Children')
    bulk = []
    for i in range(0, 100):
        jane = Child()
        jane.id = i
        jane.name = u'Child {}'.format(i)
        jone = Child()
        jone.id = i + 1000
        jone.name = u'Jone'
        john = Parent()
        john.id = i
        john.name = u'Parent {}'.format(i)
        john.children = [jane, jone]
        bulk.append(jane)
        bulk.append(jone)
        bulk.append(john)
    session.bulk_save_objects(bulk)
    session.commit()

    print('# Parents: {}'.format(session.query(Parent).count()))
    print('# Children: {}'.format(session.query(Child).count()))
    
    print('')
    print('Bulk Delete 100 Parents')
    session.query(Parent).delete()
    session.query(Child).delete()
    print('# Parents: {}'.format(session.query(Parent).count()))
    print('# Children: {}'.format(session.query(Child).count()))