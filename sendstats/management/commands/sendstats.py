from __future__ import print_function
from __future__ import absolute_import

from djcelery.app import app
from djcelery.management.base import CeleryCommand

from sendstats.bin.sendstats import SendStatsCommand

sendstats = SendStatsCommand(app=app)


class Command(CeleryCommand):
    """Run the celery sendstats."""
    option_list = CeleryCommand.option_list + sendstats.get_options()
    help = 'Run the celery sendstats'

    def handle(self, *args, **options):
        """Handle the management command."""
        sendstats.run(**options)
