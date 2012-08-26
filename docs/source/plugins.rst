Plugins
==============

booting plugins

* zabbix - zabbix post threading.Thread
* nagios - nagios post threading.Thread
* munin - munin post threading.Thread
* fluent - flutnd post threading.Thread
* EventConsumer - celery event capture - requirements


set args
--------------------

.. highlight:: bash


::

    $ celry sendstas --plugins=zabbix,nagios,munin,fluent


django setting
--------------------

.. highlight:: python


::

    # python
    CELERY_SENDSTATS_PLUGINS = (
        "path.to.class.zabbix.Zabbix", ""path.to.class.nagios.Nagios",
    )

