from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import CompositeType

Base = declarative_base()


class Person(Base):

    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)

    name = Column('name', Unicode(255))

    address = Column(
        CompositeType(
            'address_type',
            [
                Column('street', Unicode),
                Column('zip', Integer),
                Column('city', Unicode),
            ]
        )
    )


if __name__ == '__main__':

    # DB setup
    engine = create_engine('postgresql://test:test@localhost:5432/test')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session(engine)

    # create peron with a single address
    john = Person()
    john.name = u'John'
    john.address = (
        u'Examplestreet',
        53111,
        u'Bonn'
    )

    session.add(john)
    session.commit()

    # query db
    result = session.query(Person).one()
    print('Person: {}'.format(result.name))
    print('Address:')
    print(result.address.street)
    print(result.address.zip)
    print(result.address.city)
