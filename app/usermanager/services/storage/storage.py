class StorageAbstractClass:
    _conn = None

    @classmethod
    def __init__(cls, *args, **kwargs):
        try:
            cls._conn = cls.connection(cls, *args, **kwargs)
        except Exception as e:
            raise

    @classmethod
    def get_connection(cls):
        '''
        Return connect to storage.
        :return:
        '''
        return cls._conn

    def is_connected(cls) -> bool:
        pass

    def connection(cls) -> None:
        pass
