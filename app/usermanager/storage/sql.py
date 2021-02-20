from typing import Union

from .exceptions import StorageException


class SQLStorage:
    def __init__(self, storage):
        try:
            self.conn = storage.get_connection()
        except Exception as e:
            raise StorageException(e)
        self._complete = False

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

    def execute(self):
        self._complete = True

    def close(self):
        if self.conn:
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                raise StorageException(e)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    raise StorageException(e)
