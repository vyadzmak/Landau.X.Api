from concurrent.futures import ThreadPoolExecutor

_DEFAULT_POOL = ThreadPoolExecutor()

def threadpool(f, executor=None):
    def wrap(*args, **kwargs):
        return (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)
    return wrap