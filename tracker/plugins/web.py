from __future__ import print_function
from __future__ import absolute_import


from tornado.web import Application


class Site(Application):
    """ Tornado Website with multiple :class:`Application`'s.

    @celrymon ver0.5.0.

    """

    def __init__(self, applications, *args, **kwargs):
        handlers = []
        for urlprefix, application in applications:
            for urlmatch, handler in application:
                handlers.append((urlprefix + urlmatch, handler))
        kwargs["handlers"] = handlers
        super(Site, self).__init__(*args, **kwargs)
