Usage
===========

.. highlight:: bash


Start commands

::

    $ sendstats
    sendstats 0.2.3 is starting.
    Configuration ->
        . broker -> amqp://guest@127.0.0.1:5672//
        . webserver -> http://localhost:12201
    sendstats has started.


With Celery Extention
------------------------

::

    $ celery sendstats --config=celeryconfig
    sendstats 0.3.1 is starting.
    Configuration ->
        . broker -> amqp://guest@127.0.0.1:5672//
        . webserver -> http://localhost:12201
    sendstats has started.


With Django
-------------

::

    $ python manage.py celery sendstats --settings=project.settings --pythonpath=~/.virtualenvs/project/


