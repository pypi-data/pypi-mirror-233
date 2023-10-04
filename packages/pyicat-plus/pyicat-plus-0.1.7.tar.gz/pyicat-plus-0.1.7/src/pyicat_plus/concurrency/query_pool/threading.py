from typing import Any, Callable, Dict, Optional
from time import time
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError
from threading import RLock

from ...utils.maxsizedict import MaxSizeDict


class QueryPool:
    """Query pool for gevent non-cooperative calls."""

    def __init__(
        self, timeout: Optional[float] = None, maxqueries: Optional[int] = None
    ):
        """
        :param timeout: The default timeout of a call before returning/raising the previous result.
        :param maxqueries: The maximal number of different queries to store results from.
                           A query can differ in terms of function and/or arguments.
        """
        self.__pool = ThreadPoolExecutor(max_workers=10000)
        if timeout is None:
            timeout = 0.1
        self.timeout = timeout
        self.__futures: Dict[tuple, Future] = dict()
        if maxqueries:
            self.__lock = RLock()
            self.__results = MaxSizeDict(maxsize=maxqueries)
        else:
            self.__lock = None
            self.__results = dict()

    @contextmanager
    def _lock(self):
        if self.__lock is None:
            yield
        else:
            with self.__lock:
                yield

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
                    result = query(*args, **kwargs)
                    with self._lock():
                        self.__results[call_id] = False, result
                except BaseException as e:
                    with self._lock():
                        self.__results[call_id] = True, e
                    raise
                finally:
                    with self._lock():
                        self.__futures.pop(call_id, None)

            with self._lock():
                self.__futures[call_id] = future = self.__pool.submit(wrapper)

        if timeout is None:
            timeout = self.timeout
        try:
            future.result(timeout=timeout)
        except TimeoutError:
            pass
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
        try:
            with self._lock():
                futures = list(self.__futures.values())
            for future in futures:
                t0 = time()
                future.result(timeout=timeout)
                timeout = max(timeout - time() + t0, 0)
        except TimeoutError:
            return False
        return True
