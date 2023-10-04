from typing import Any, Callable, Dict, Optional
import gevent

from ...utils.maxsizedict import MaxSizeDict


class CancelQuery(gevent.GreenletExit):
    pass


class QueryPool:
    """Query pool for gevent cooperative calls."""

    def __init__(
        self, timeout: Optional[float] = None, maxqueries: Optional[int] = None
    ):
        """
        :param timeout: The default timeout of a call before returning/raising the previous result.
        :param maxqueries: The maximal number of different queries to store results from.
                           A query can differ in terms of function and/or arguments.
        """
        if not gevent:
            raise RuntimeError("QueryPool requires gevent")
        if timeout is None:
            timeout = 0.1
        self.timeout = timeout
        self.__futures: Dict[tuple, gevent.Greenlet] = dict()
        if maxqueries:
            self.__results = MaxSizeDict(maxsize=maxqueries)
        else:
            self.__results = dict()

    def execute(
        self,
        query: Callable,
        args: Optional[tuple] = tuple(),
        kwargs: Optional[dict] = None,
        timeout: Optional[float] = None,
        default=None,
    ) -> Any:
        """
        :param query:
        :param args: positional arguments
        :param kwargs: named arguments
        :param timeout: the timeout of a call before returning/raising the previous result
        :param default: the default value in case there is no previous result
        :returns: the result of the query or the default value
        :raises: the exception from the query
        """
        if kwargs is None:
            kwargs = dict()
        call_id = query, args, tuple(kwargs.items())
        future = self.__futures.get(call_id)
        if future is None:

            def wrapper():
                try:
                    self.__results[call_id] = False, query(*args, **kwargs)
                except BaseException as e:
                    self.__results[call_id] = True, e
                    raise
                finally:
                    self.__futures.pop(call_id, None)

            future = gevent.Greenlet(wrapper)
            self.__futures[call_id] = future
            future.start()
        if timeout is None:
            timeout = self.timeout
        future.join(timeout=timeout)
        result = self.__results.get(call_id, None)
        if result is None:
            return default
        is_error, result = result
        if is_error:
            raise result
        return result

    def wait(self, timeout=None) -> bool:
        """
        :param timeout:
        :returns: `True` when all queries finished, `False` otherwise
        """
        futures = list(self.__futures.values())
        finished = gevent.joinall(futures, timeout=timeout)
        return len(futures) == len(finished)

    def cancel(self, timeout=None, block=True) -> Optional[bool]:
        """
        :param block:
        :param timeout: only applies when `block=True`
        :returns: `None` when `block=False`, `True` when all queries are
                  cancelled and `False` otherwise
        """
        futures = list(self.__futures.values())
        if not block:
            gevent.killall(futures, exception=CancelQuery, block=False)
            return
        try:
            with gevent.Timeout(timeout) as local_timeout:
                gevent.killall(futures, exception=CancelQuery, timeout=timeout)
        except gevent.Timeout as raised_timeout:
            if raised_timeout is not local_timeout:
                raise
            return False
        return True
