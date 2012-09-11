from __future__ import print_function
from __future__ import absolute_import


from celerymon.handlers.api import api_handler


def baseHandler(plugin):
    """ web handler """
    @api_handler
    def receive(request=None, *args, **kwargs):
        """ receiver """
        event = plugin.pop_event()
        plugin.logging(event)

        if not plugin.verbose:
            event.pop("workers")
            event.pop("tasks")
        return event

    return receive

