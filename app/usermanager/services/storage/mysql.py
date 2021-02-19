from MySQLdb import _mysql

from .sql import SQLStorage
from .storage import StorageAbstractClass


class MySQL(StorageAbstractClass):
    def connection(cls, *args, **kwargs):
        return _mysql.connect(*args, **kwargs)

    def is_connected(self):
        return True if self._conn else False


class MySQLStorage(SQLStorage):
    pass
