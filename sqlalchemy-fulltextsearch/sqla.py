from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import Session

Base = declarative_base()


class Book(Base):

    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)

    title = Column(Unicode(255), nullable=False)

    description = Column(Unicode(255), nullable=False)

#    book_authors = relationship(
#        "BookAuthor",
#        cascade="all, delete-orphan",
#        backref='book'
#    )

    def __init__(self, title):
        self.title = title


class Author(Base):

    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

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
    rank = Column(Unicode)

    def __init__(self, author, rank=None):
        self.author = author
        self.rank = rank

    author = relationship(Author, lazy='joined')


def setup_search(event, schema_item, bind):
    """ Automatically run when SQLAlchemy creates the tables e.g. by running
    Base.metadata.create_all(bind=db) """
    # We don't want sqlalchemy to know about this column so we add it
    # externally.
    bind.execute("alter table book add column search_vector tsvector")

    # This indexes the tsvector column
    bind.execute("""create index book_search_index on book
                    using gin(search_vector)""")

    # This sets up the trigger that keeps the tsvector column up to date.
    bind.execute("""create trigger book_search_update before update or
                    insert on book
                    for each row execute procedure
                    tsvector_update_trigger('search_vector',
                                            'pg_catalog.english',
                                            'description',
                                            'title')""")

# We want to call setup_search after the book has been created.
Book.__table__.append_ddl_listener('after-create', setup_search)


def search(searchterms):
    """ Given the user's input, returns a list of 3-tuples: blog post object,
    a list of fragments containing search terms with <span class="highlight">
    </span> around the search terms and the blog title also containing
    <span class="highlight"></span> around each search term. """

    # search_vector is a ts_vector column. To search for terms, you use the
    # @@ operator. plainto_tsquery turns a string into a query that can be
    # used with @@. So this adds a where clause like "WHERE search_vector
    # @@ plaint_tsquery(<search string>)"
    query = session.query(Book).filter('book.search_vector '\
                                 '@@ plainto_tsquery(:terms)')

    # This binds the :terms placeholder to the searchterms string. User input
    # should always be put into queries this way to prevent SQL injection.
    query = query.params(terms=searchterms)

    # This calls ts_rank_cd with the search_vector and the query and gives a ranking
    # to each row. We order by this descending. Again, the :terms placeholder is used
    # to insert user input.
    #q = q.order_by('ts_rank_cd(book.search_vector, '\
    #             'plainto_tsquery(:terms)) DESC')

    # Because of the two add_column calls above, the query will return a 3-tuple
    # consisting of the actual entry objects, the fragments for the contents and
    # the highlighted headline. In order to make the fragments a list, we split them
    # on '|||' - the FragmentDelimiter.
    #return [(entry, fragments.split('|||'), title) for entry, fragments, title in q]
    return query.all()


if __name__ == '__main__':
    engine = create_engine(
        'postgresql://test:test@localhost:5432/test',
        echo=True
    )
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session(engine)

    # create two authors
    chomsky = Author('Noam Chomsky')
    miller = Author('George A . Miller')
    session.add_all([chomsky, miller])
    session.commit()

    # create an book with a single author
    book1 = Book('Syntactic Structures')
    book1.description = 'Syntactic Structures is a book in linguistics by American linguist Noam Chomsky, first published in 1957'  # noqa
    # book1.book_authors.append(BookAuthor(chomsky))
    session.add(book1)
    session.commit()

    # create a book with two authors
    book2 = Book('Finite State Languages')
    book2.description = 'A finite state language is a finite or infinite set of strings (sentences) of symbols (words) generated by a finite set of rules (the grammar).'  # noqa
    # book2.book_authors.append(BookAuthor(chomsky, 'primary'))
    # book2.book_authors.append(BookAuthor(miller, 'secondary'))
    session.add(book2)
    session.commit()

    # query the book, print authors with their rank
    # books = session.query(Book).all()
    # for book in books:
    #    print('%s:' % book.title)
    #    print([
    #        (book_author.author.name, book_author.rank)
    #        for book_author in book.book_authors
    #    ])

    print search('finite')[0].title
