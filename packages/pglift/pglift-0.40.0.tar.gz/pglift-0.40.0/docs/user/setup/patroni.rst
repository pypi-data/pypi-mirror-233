Patroni
=======

PostgreSQL high availability is achieved by using the `patroni` plugin of
pglift. This needs to be set up through a non-``null`` value for the
``patroni`` key in site settings:

.. code-block:: yaml
   :caption: settings.yaml

    patroni: {}

With the above settings, pglift assumes that an *open* etcd server is
available at ``127.0.0.1:2379``. It may be required to configure the etcd
hosts address:

.. code-block:: yaml
   :caption: settings.yaml

    patroni:
      etcd:
        hosts:
        - 192.168.60.21:2379
        - 192.168.60.21:2380

Security
--------

Protecting Etcd
~~~~~~~~~~~~~~~

Via site settings, it's possible to secure communication between Patroni
and etcd via TLS.

The settings would look like the following:

.. code-block:: yaml
   :caption: settings.yaml

    patroni:
      […]
      etcd:
        protocol: https
        cacert: /path/to/cacert.crt
        cert: /path/to/client.crt
        key: /path/to/client.key
        username: myuser

Those settings are actually copied to the etcd section in Patroni YAML
configuration file that pglift generates at instance creation.

At least the ``protocol: https`` should be specified to enable TLS encryption.
Unless the root certificate for the authority is available in system's store,
the ``cacert`` should be specified as well.

Then, client certificates ``cert`` and ``key`` can be specified to enable TLS
authentication provided that the etcd server runs with client certificate
authentication enabled (``--client-cert-auth`` and ``--trusted-ca-file``
command-line options for etcd); this configuration provides a global
authentication, but no role-based security.

For role-based authorization, and provided the etcd server has roles and users
defined, and authentication enabled, the ``username`` key should be set. This
comes along with the ``--patroni-etcd-{username,password}`` command-line
options from ``pglift instance create``.

.. warning::
   Basic-authentication works by writing Etcd username and password to the
   Patroni YAML configuration; pglift generates the file with owner-read
   permission ``600`` though.

.. note::
   Basic authentication takes precedence on the client certificates method so
   both methods should not be used together.

Protecting the REST API
~~~~~~~~~~~~~~~~~~~~~~~

To secure the patroni's REST API, the following parameters can be set:

.. code-block:: yaml
   :caption: settings.yaml

    patroni:
      […]
      restapi:
        cafile: /path/to/cacert.crt
        certfile: /path/to/client.crt
        keyfile: /path/to/client.key
        verify_client: optional

``verify_client`` must be set to either ``required`` or ``optional`` if
certificates are set. Please refer to `patroni' s official documentation
<https://patroni.readthedocs.io/en/latest/yaml_configuration.html#rest-api>`_.

Those settings are actually copied to the ``restapi`` section in Patroni YAML
configuration file that pglift generates at instance creation.

Watchdog support
----------------

One can activate watchdog devices support via site settings. Please refer to
patroni `configuration
<https://patroni.readthedocs.io/en/latest/yaml_configuration.html#watchdog>`_
and `watchdog <https://patroni.readthedocs.io/en/latest/watchdog.html>`_
documentation.

Here's an example of settings for watchdog:

.. code-block:: yaml
   :caption: settings.yaml

    patroni:
      […]
      watchdog:
        mode: required
        device: /dev/watchdog
        safety_margin: 5

pg_rewind support
-----------------

``pg_rewind`` can be activated by adding the following settings:

.. code-block:: yaml
   :caption: settings.yaml

    patroni:
      […]
      use_pg_rewind: true

The corresponding setting will go in the `patroni.postgresql
<https://patroni.readthedocs.io/en/latest/yaml_configuration.html#postgresql>`_
section in patroni configuration file.
