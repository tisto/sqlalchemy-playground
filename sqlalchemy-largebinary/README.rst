==============================================================================SQLALCHEMY / POSTGRES LARGE BINARY OBJECTS
==============================================================================

Prerequisits
------------

Create DB user and database::

  $ sudo su postgres
  $ createuser test
  $ createdb test

Set password and grant user db access:

  $ psql
  # GRANT ALL PRIVILEGES ON DATABASE test TO test;
  # ALTER USER dkg WITH PASSWORD 'test';
  # \q

Allow local connections (/etc/postgresql/9.3/main/pg_hba.conf)::

  # Put your actual configuration here
  # ----------------------------------
  #
  # If you want to allow non-local connections, you need to add more
  # "host" records.  In that case you will also need to make PostgreSQL
  # listen on a non-local interface via the listen_addresses
  # configuration parameter, or via the -i or -h command line switches.

  local   test            test                                   md5

Reload Postgres configuration (as root)::

  $ sudo /etc/init.d/postgresql reload

Test database connection (as regular user)::

  $ psql test test


Setup
-----

Create virtual environment and install dependencies::

  $ virtualenv .env
  $ source .env/bin/activate
  $ pip install -r requirements.txt

Run example::

  $ python sqla.py

