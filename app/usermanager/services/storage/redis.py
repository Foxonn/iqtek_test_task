import redis
from redis.client import Pipeline

from .storage import StorageAbstractClass
from .exceptions import StorageException


class Redis(StorageAbstractClass):
    def connection(self, *args, **kwargs):
        return redis.Redis(*args, **kwargs)

    def is_connected(self):
        return self._conn.ping()


class RedisStorage(Pipeline):
    def __init__(self, storage, *args, **kwargs):
        try:
            self.conn = storage.get_connection()
        except Exception as e:
            raise StorageException(e)

        super(RedisStorage, self).__init__(
            self.conn.connection_pool,
            self.conn.response_callbacks,
            transaction=True,
            shard_hint=None,
        )
