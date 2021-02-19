import redis

from .storage import StorageAbstractClass


class Redis(StorageAbstractClass):
    def connection(self, *args, **kwargs):
        return redis.Redis(*args, **kwargs)

    def is_connected(self):
        return self._conn.ping()
