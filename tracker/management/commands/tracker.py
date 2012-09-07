from __future__ import print_function
from __future__ import absolute_import

from djcelery.app import app
from djcelery.management.base import CeleryCommand

from tracker.bin.tracker import TrackerCommand

tracker = TrackerCommand(app=app)


class Command(CeleryCommand):
    """Run the celery tracker."""
    option_list = CeleryCommand.option_list + tracker.get_options()
    help = 'Run the celery tracker'

    def handle(self, *args, **options):
        """Handle the management command."""
        tracker.run(**options)
