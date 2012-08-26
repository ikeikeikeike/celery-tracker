#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import with_statement

import sys
# import os
import traceback
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
from celerymon.bin.celerymon import STARTUP_INFO_FMT
from celery.utils import LOG_LEVELS
# from celerymon.bin import celerymon

# from .. import service
from .. import get_version
from ..service import SendStatsService


def csv_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))


# TODO: Original Service
#celerymon.MonitorService = service.MonitorService
#SendStatsCommand = celerymon.MonitorCommand
#SendStatsCommand.namespace = "sendstats"
#SendStatsCommand.preload_options = Command.preload_options + daemon_options("sendstats.pid")
#SendStatsCommand.version = get_version()

class SendStatsCommand(Command):
    namespace = "sendstats"
    preload_options = Command.preload_options + daemon_options("{0}.pid".format(namespace))
    version = get_version()

    def run(self, loglevel="ERROR", logfile=None, http_port=12201,
            http_address='', app=None, detach=False, pidfile=None,
            uid=None, gid=None, umask=None, working_directory=None,
            plugins=None, debug=False, **kwargs):
        print("{0} {1} is starting.".format(self.namespace, self.version, ))
        app = self.app
        workdir = working_directory

        # Setup logging
        if not isinstance(loglevel, int):
            loglevel = LOG_LEVELS[loglevel.upper()]

        # debug server
        print(STARTUP_INFO_FMT % {
            "http_port": http_port,
            "http_address": http_address or "localhost",
            "conninfo": app.broker_connection().as_uri(),
        })

        print("{0} has started.".format(self.namespace))
        set_process_title("{0}".format(self.namespace), info=strargv(sys.argv))

        if detach:
            with detached(logfile, pidfile, uid, gid, umask, workdir):
                self._run_sendstats(loglevel, logfile, http_port, http_address, plugins)
        else:
            self._run_sendstats(
                loglevel, logfile, http_port, http_address, plugins)

    def _run_sendstats(self, loglevel, logfile, http_port, http_address, plugins):
        app = self.app

        app.log.setup_logging_subsystem(loglevel=loglevel, logfile=logfile)
        logger = app.log.get_default_logger(name="celery.{0}".format(self.namespace))
        monitor = SendStatsService(
            logger=logger, http_port=http_port, http_address=http_address, plugins=plugins)
        try:
            monitor.start()
        except Exception, exc:
            logger.error("%s raised exception %r\n%s" % (self.namespace, exc, traceback.format_exc()))
        except KeyboardInterrupt:
            pass

    def get_options(self):
        conf = self.app.conf
        return super(SendStatsCommand, self).get_options() + (
            Option('-p', '--plugins',
                   action='callback', type='string', default=conf.CELERY_SENDSTATS_PLUGINS,
                   callback=csv_callback,
                   help=("List of plugins to enable for this threading, separated by\n"
                         "comma. By default all configured plugins are enabled.\n"
                         "Example: -p zabbix,logging,fluent")),
            Option('-l', '--loglevel',
                   default=conf.CELERY_SENDSTATS_LOG_LEVEL,
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

    class MonitorDelegate(Delegate):
        Command = SendStatsCommand
except ImportError:
    class MonitorDelegate(object):  # noqa
        pass


def main():
    sendstats = SendStatsCommand()
    sendstats.execute_from_commandline()


if __name__ == "__main__":
    main()
