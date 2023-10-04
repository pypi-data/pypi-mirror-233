try:
    import gevent
except ImportError:
    gevent = None
else:
    from gevent.monkey import is_anything_patched

    if not is_anything_patched():
        gevent = None


if gevent is None:
    import threading
    from subprocess import TimeoutExpired
    from queue import Queue, Empty

    def spawn(func, *args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    def wait_process(process, timeout) -> bool:
        """
        :param process: A process object from `subprocess` or `psutil`
        """
        try:
            process.wait(timeout)
            return True
        except (TimeoutError, TimeoutExpired):
            return False

else:
    from gevent import spawn  # noqa F401
    from gevent.queue import Queue, Empty

    def wait_process(process, timeout) -> bool:
        """
        :param process: A process object from `subprocess` or `psutil`
        """
        try:
            with gevent.Timeout(timeout) as local_timeout:
                # gevent timeout has to be used here
                # See https://github.com/gevent/gevent/issues/622
                process.wait()
            return True
        except gevent.Timeout as raised_timeout:
            if local_timeout is not raised_timeout:
                raise
            return False


def flush_queue(q: Queue):
    while True:
        try:
            yield q.get(timeout=0)
        except Empty:
            break
