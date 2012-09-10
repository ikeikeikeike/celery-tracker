from __future__ import print_function
from __future__ import absolute_import


from celerymon.handlers.api import api_handler


def baseHandler(plugin):

    @api_handler
    def receive(request=None, *args, **kwargs):
        event = plugin.pop_event()
        plugin.logging(event)
        return event

    return receive

