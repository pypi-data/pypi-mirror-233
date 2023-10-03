Databases backup and restore
----------------------------

`pglift` provides a streamlined way to perform logical database backup.
Please refer to :ref:`database dumps<database-dumps>`. Database restore,
however, is left to the user's responsibility.

Programs ``pg_dump`` and ``pg_restore`` can also be used directly through ``pglift
instance exec`` command.

.. code-block:: console

    $ pglift instance exec 14/main -- pg_dump -Fd mydb -j4 -f mydb.dump
    $ pglift instance exec 14/main -- pg_restore -d postgres --clean --create mydb.dump
