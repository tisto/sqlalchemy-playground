"""ordering_list.py
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


class Slide(Base):
    __tablename__ = 'slide'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    bullets = relationship(
        "Bullet",
        order_by="Bullet.position",
        collection_class=ordering_list('position')
    )


class Bullet(Base):
    __tablename__ = 'bullet'
    id = Column(Integer, primary_key=True)
    slide_id = Column(Integer, ForeignKey('slide.id'))
    position = Column(Integer)
    text = Column(String)


if __name__ == '__main__':
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)

    session = Session(engine)

    slide = Slide()
    slide.bullets.append(Bullet())
    slide.bullets.append(Bullet())
    assert slide.bullets[1].position == 1

    slide.bullets.insert(1, Bullet())
    assert slide.bullets[2].position == 2
