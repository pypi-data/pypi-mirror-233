.. _install:

Installation
============

pglift can be installed from PyPI.

Using `pipx <https://pypa.github.io/pipx/>`_ is certainly the simplest way to
install pglift::

    $ pipx install pglift

Otherwise, it is recommended to use a dedicated virtualenv:
::

    $ python3 -m venv .venv
    $ . .venv/bin/activate
    (.venv) $ pip install 'pip>=20.3'

and then proceed with actual installation as:
::

    (.venv) $ pip install pglift

Once installed, the ``pglift`` command should be available:

::

    Usage: pglift [OPTIONS] COMMAND [ARGS]...

      Deploy production-ready instances of PostgreSQL

    Options:
      -L, --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                      Set log threshold (default to INFO when
                                      logging to stderr or WARNING when logging to
                                      a file).
      -l, --log-file LOGFILE          Write logs to LOGFILE, instead of stderr.
      --interactive / --non-interactive
                                      Interactively prompt for confirmation when
                                      needed (the default), or automatically pick
                                      the default option for all choices.
      --version                       Show program version.
      --help                          Show this message and exit.

    Commands:
      instance  Manage instances.
      pgconf    Manage configuration of a PostgreSQL instance.
      role      Manage roles.
      database  Manage databases.

Site configuration
------------------

An extra step is usually required as part of :ref:`site
configuration<site-configuration>` to install extra data files (like base
configuration files for satellite components or systemd unit templates). This
is done by invoking ``pglift site-configure install`` command. Conversely,
upon uninstalling, ``pglift site-configure uninstall`` command may be invoked.

If installation is incomplete or the command has not been run at all, any
operation will fail with an error message suggesting to perform a proper
installation.

.. warning::
   The exact result of ``site-configure`` commands depends on :ref:`site
   settings <settings>`; so changing those after having run the ``install``
   command will quite likely break the site installation (and probably make
   already created instances non-functional).

Runtime dependencies
--------------------

pglift operates PostgreSQL and a number of satellite components, each
available as independent software packages. Thus, depending of selected
components (see :ref:`site settings <settings>`), the following packages might
be needed:

- ``postgresql``
- ``pgbackrest``
- ``prometheus-postgres-exporter``
- ``powa`` (with ``pg_qualstats`` and ``pg_stat_kcache``)
- ``temboard-agent``
- ``patroni``
