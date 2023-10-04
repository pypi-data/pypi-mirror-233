"""Query pools let a query run in the background when it
doesn't return within a given timeout. In that case the
result of the previous query is returned or raised. If
there is no result, the default value is returned.
"""

from .. import gevent

if gevent is None:
    from .threading import QueryPool  # noqa F401
else:
    from .gevent import QueryPool  # noqa F401
