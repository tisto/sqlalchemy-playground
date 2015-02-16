==============================================================================
SQLAlchemy Association Proxy
==============================================================================

The SQLAlchemy Association Proxy should be used when you are trying to model a relationship with additional attributes.

Imagine you have a 'Book' type and an 'Author' type and you want to model the Book Author relationship with primary and secondary authors separated.

Setup::

  $ virtualenv-2.7 .env
  $ source .env/bin/activate
  $ pip install -r requirements.txt

Run Tests::

  $ py.test
