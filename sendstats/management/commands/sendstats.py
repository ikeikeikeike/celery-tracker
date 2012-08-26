from __future__ import print_function
from __future__ import absolute_import

from djcelery.app import app
from djcelery.management.base import CeleryCommand

from sendstats.bin.sendstats import SendStatsCommand

monitor = SendStatsCommand(app=app)


class Command(CeleryCommand):
    """Run the celery monitor."""
    option_list = CeleryCommand.option_list + monitor.get_options()
    help = 'Run the celery monitor'

    def handle(self, *args, **options):
        """Handle the management command."""
        monitor.run(**options)
