Plugins
==========

Booting plugins

* Zabbix - zabbix post threading.Thread
* Fluent - Flutnd post threading.Thread
* Nagios - Nagios post threading.Thread
* Munin - Munin post threading.Thread

Set args
--------------------

.. highlight:: bash


::

    $ celry sendstas --plugins=zabbix,nagios,munin,fluent


Django setting
--------------------

.. highlight:: python


::

    # python
    CELERY_SENDSTATS_PLUGINS = (
        "path.to.class.zabbix.Zabbix", ""path.to.class.nagios.Nagios",
    )


Reference
--------------------


Base
~~~~~~~~~~

.. autoclass:: sendstats.plugins.base.BasePlugin
   :members:

Zabbix
~~~~~~~

.. autoclass:: sendstats.plugins.zabbix.ZabbixPlugin
   :members:

Fluent
~~~~~~~~~~

.. autoclass:: sendstats.plugins.fluent.FluentPlugin
   :members:


