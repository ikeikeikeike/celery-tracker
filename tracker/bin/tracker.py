#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import with_statement

# import os
import sys
import traceback
from pprint import pprint
from celery.platforms import (
    set_process_title,
    strargv,
    detached
)
from celery.bin.base import (
    Command,
    Option,
    daemon_options
)
#from celerymon.bin.celerymon import STARTUP_INFO_FMT
from celery.utils import LOG_LEVELS


from .. import get_version
from ..service import TrackerService


def csv_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))


class TrackerCommand(Command):
    namespace = "tracker"
    preload_options = Command.preload_options + daemon_options("{0}.pid".format(namespace))
    version = get_version()

    def run(self, loglevel="ERROR", logfile=None, http_port=12201,
            http_address='', app=None, detach=False, pidfile=None,
            uid=None, gid=None, umask=None, working_directory=None,
            plugins=None, storage=None, debug=False, **kwargs):
        print("{0} {1} is starting.".format(self.namespace, self.version, ))
        app = self.app
        workdir = working_directory

        # Setup logging
        if not isinstance(loglevel, int):
            loglevel = LOG_LEVELS[loglevel.upper()]

        print("")
        print("Using below's plugins.")
        pprint(plugins)

        # debug server
#        print(STARTUP_INFO_FMT % {
#            "http_port": http_port,
#            "http_address": http_address or "localhost",
#            "conninfo": app.broker_connection().as_uri(),
#        })

        print("")
        print("{0} has started.".format(self.namespace))
        set_process_title("{0}".format(self.namespace), info=strargv(sys.argv))

        if detach:
            with detached(logfile, pidfile, uid, gid, umask, workdir):
                self._run_tracker(
                    loglevel, logfile, http_port,
                    http_address, plugins=plugins, storage=storage)
        else:
            self._run_tracker(
                loglevel, logfile, http_port,
                http_address, plugins=plugins, storage=storage)

    def _run_tracker(self, loglevel, logfile, http_port,
                       http_address, plugins, storage):
        app = self.app
        app.log.setup_logging_subsystem(loglevel=loglevel, logfile=logfile)

        logger = app.log.get_default_logger(name="celery.{0}".format(self.namespace))
        tracker = TrackerService(
            logger=logger, http_port=http_port,
            http_address=http_address, plugins=plugins, storage=storage)
        try:
            tracker.start()
        except Exception, exc:
            logger.error("%s raised exception %r\n%s" % (
                self.namespace, exc, traceback.format_exc()))
        except KeyboardInterrupt:
            pass

    def get_options(self):
        from ..configs import celeryconfig as gconf
        conf = self.app.conf

        return super(TrackerCommand, self).get_options() + (
            Option('-p', '--plugins',
                   action='callback', type='string',
                   default=getattr(
                       conf, "CELERY_TRACKER_PLUGINS", gconf.CELERY_TRACKER_PLUGINS),
                   callback=csv_callback,
                   help=("List of plugins to enable for this process, separated by\n"
                         "comma. By default all configured plugins are enabled.\n"
                         "Example: -p zabbix,logging,fluent")),
            Option('-s', '--storage',
                   action='store', type='string',
                   default=getattr(conf, "CELERY_TRACKER_STORAGE", ""),
                   help="file storage path. (default: memory)"),
            Option('-l', '--loglevel',
                   default=getattr(
                       conf, "CELERY_TRACKER_LOG_LEVEL", gconf.CELERY_TRACKER_LOG_LEVEL),
                   action="store", dest="loglevel",
                   help="Choose between DEBUG/INFO/WARNING/ERROR/CRITICAL."),
            Option('-P', '--port',
                   action="store", type="int", dest="http_port", default=12201,
                   help="Port the webserver should listen to."),
            Option('-B', '--bind',
                   action="store", type="string", dest="http_address",
                   default="",
                   help="Address webserver should listen to. Default (any)."),
            Option('-D', '--detach',
                   action="store_true", dest="detach",
                   default=False,
                   help="Run as daemon.")
        )


try:
    # celery 3.x extension command
    from celery.bin.celery import Delegate

    class TrackerDelegate(Delegate):
        Command = TrackerCommand
except ImportError:
    class TrackerDelegate(object):
        pass


def main():
    tracker = TrackerCommand()
    tracker.execute_from_commandline()


if __name__ == "__main__":
    main()
