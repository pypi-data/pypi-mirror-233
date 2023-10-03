Major online upgrades
---------------------

In the following, we illustrate how to perform an online upgrade of a database
from PostgreSQL version 12 to version 15 with Ansible and pglift. The source
database ``app`` lives in instance ``12/old``:

.. code-block:: console

    $ pglift instance create old --version=12 --port=5499
    INFO     initializing PostgreSQL
    INFO     configuring PostgreSQL authentication
    INFO     configuring PostgreSQL
    INFO     starting PostgreSQL 12-old
    $ pglift role -i old create app --password
    Role password:
    Repeat for confirmation:
    INFO     creating role 'app'
    $ pglift database -i old create app --owner app
    INFO     creating 'app' database

and we're filling it with some data:

.. code-block:: console

    $ pglift database -i old run -d app 'CREATE TABLE books (title TEXT)'
    INFO     running "CREATE TABLE books (title TEXT)" on app database of 12/old
    INFO     CREATE TABLE
    $ pglift database -i old run -d app "ALTER TABLE books OWNER TO app"
    INFO     running "ALTER TABLE books OWNER TO app" on app database of 12/old
    INFO     ALTER TABLE
    $ pglift database -i old run -d app "INSERT INTO books VALUES ('On the road'), ('Big Sur')"
    INFO     running "INSERT INTO books VALUES ('On the road'), ('Big Sur')" on app
             database of 12/old
    INFO     INSERT 0 2

Let's prepare it for logical replication by:

1. adjusting the ``app`` role with ``LOGIN`` and ``REPLICATION`` options, and,
2. adding a ``publication`` to the source database.

We'll be doing this through the following Ansible playbook which also sets up
the target instance named ``new`` (in PostgreSQL version 15):

.. literalinclude:: ../ansible/online-upgrade.yml
    :language: yaml
    :caption: online-upgrade.yml

Note that the target database ``app`` is:

1. initialized as a clone of the source database, but only for data
   definitions (the ``clone.schema_only: true`` option),
2. configured with a ``subscription`` matching the ``publication`` on the
   source database.

Also note that the source instance needs ``wal_level=logical`` for logical
replication to work.

Once this playbook applied, we should get two instances locally:

.. code-block:: console

    $ ps xf
    60533 pts/2    S      0:00 /usr/lib/postgresql/15/bin/postgres -D /srv/pgsql/15/new/data
    60535 ?        Ss     0:00  \_ postgres: new: logger
    60536 ?        Ss     0:00  \_ postgres: new: checkpointer
    60537 ?        Ss     0:00  \_ postgres: new: background writer
    60539 ?        Ss     0:00  \_ postgres: new: walwriter
    60540 ?        Ss     0:00  \_ postgres: new: autovacuum launcher
    60541 ?        Ss     0:00  \_ postgres: new: logical replication launcher
    60560 ?        Ss     0:00  \_ postgres: new: logical replication worker for subscription 16387
    60446 pts/2    S      0:00 /usr/lib/postgresql/12/bin/postgres -D /srv/pgsql/12/old/data
    60448 ?        Ss     0:00  \_ postgres: old: logger
    60450 ?        Ss     0:00  \_ postgres: old: checkpointer
    60451 ?        Ss     0:00  \_ postgres: old: background writer
    60452 ?        Ss     0:00  \_ postgres: old: walwriter
    60453 ?        Ss     0:00  \_ postgres: old: autovacuum launcher
    60454 ?        Ss     0:00  \_ postgres: old: stats collector
    60455 ?        Ss     0:00  \_ postgres: old: logical replication launcher
    60561 ?        Ss     0:00  \_ postgres: old: walsender app ::1(46192) idle

with logical replication in place:

.. code-block:: console

    $ pglift database -i new run -d app 'TABLE books' -o json
    INFO     running "TABLE books" on app database of 15/new
    INFO     SELECT 2
    {
      "app": [
        {
          "title": "On the road"
        },
        {
          "title": "Big Sur"
        }
      ]
    }


Once the replication is done and everything is in sync, the subscription on
the target database can be *disabled* (or it can be dropped):

.. code-block:: yaml
   :emphasize-lines: 10

    - name: new instance
      dalibo.pglift.instance:
        ...
        databases:
          - name: app
            owner: app
            ...
            subscriptions:
              - name: migrate
                enabled: false
                connection:
                  conninfo: "host=localhost user=app port=5499"
                  password: "{{ app_password }}"
                publications:
                  - migrate
