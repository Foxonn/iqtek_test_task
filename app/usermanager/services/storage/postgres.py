import psycopg2

from .storage import StorageAbstractClass


class Postgres(StorageAbstractClass):
    def connection(self, *args, **kwargs):
        return psycopg2.connect(*args, **kwargs)

    def is_connected(self):
        return True if self._conn else False
