from typing import List, Union
from abc import ABCMeta, abstractmethod
import pickle

from redis.client import Pipeline
import hashlib

from app.usermanager.services.entities.user import User
from app.usermanager.services.storage.exceptions import StorageException
from app.usermanager.services.storage import (
    Postgres,
    Redis,
    StorageAbstractClass,
)
from app.usermanager.settings import DATABASES


class RedisStorage(Pipeline):
    def __init__(self, storage: Redis, *args, **kwargs):
        try:
            self.conn = storage.get_connection()
        except Exception as e:
            raise StorageException()
        self._complete = False

        super(RedisStorage, self).__init__(
            self.conn.connection_pool,
            self.conn.response_callbacks,
            transaction=True,
            shard_hint=None,
        )


class SQLStorage:
    def __init__(self, storage: Postgres):
        try:
            self.conn = storage.get_connection()
        except Exception as e:
            raise StorageException()
        self._complete = False

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

    def complete(self):
        self._complete = True

    def close(self):
        if self.conn:
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                raise StorageException()
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    raise StorageException()


class UserRepositoryAbstractClass(metaclass=ABCMeta):

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> bool:
        pass

    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def get(self, id: int) -> User:
        pass


class SQLUserStorage(SQLStorage, UserRepositoryAbstractClass):
    def get_all(self) -> List[User]:
        try:
            c = self.conn.cursor()

            query = "SELECT * FROM users;"

            c.execute(query)

            rows = c.fetchall()

            users = []

            for row in rows:
                id, first_name, middle_name, last_name = row
                users.append(
                    User(
                        id=id,
                        first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                    )
                )

            return users
        except Exception as e:
            raise StorageException(e)

    def add(self, user: User) -> User:
        try:
            c = self.conn.cursor()

            query = """
                INSERT INTO users (first_name, middle_name, last_name)
                VALUES('{first_name}', '{middle_name}', '{last_name}')
                RETURNING id;
            """.format(
                first_name=user.first_name,
                middle_name=user.middle_name,
                last_name=user.last_name,
            )

            c.execute(query)

            user.id = c.fetchone()[0]

            return user
        except Exception as e:
            raise StorageException(e)

    def get(self, id: int) -> Union[User, bool]:
        try:
            c = self.conn.cursor()

            query = "SELECT * FROM users WHERE id={id};".format(id=id)

            c.execute(query)

            row = c.fetchone()

            if not row:
                raise StorageException(f'User id={id} not found!')

            id, first_name, middle_name, last_name = row

            user = User(
                id=id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
            )

            return user
        except Exception as e:
            raise StorageException(e)

    def delete(self, id: int) -> bool:
        try:
            c = self.conn.cursor()

            query = "DELETE FROM users WHERE id={id};".format(id=id)

            c.execute(query)

            if c.rowcount:
                return True
            raise StorageException(f'User id={user.id} not found!')
        except Exception as e:
            raise StorageException(e)

    def update(self, user: User) -> bool:
        try:
            c = self.conn.cursor()

            query = """
                UPDATE users
                SET
                    first_name='{first_name}',
                    middle_name='{middle_name}',
                    last_name='{last_name}'
                WHERE id={id};
            """.format(
                id=user.id,
                first_name=user.first_name,
                middle_name=user.middle_name,
                last_name=user.last_name,
            )

            c.execute(query)

            if c.rowcount:
                return True
            raise StorageException(f'User id={user.id} not found!')
        except Exception as e:
            raise StorageException(e)


class PostgresUserRepository(SQLUserStorage):
    pass


class RedisUserRepository(RedisStorage, UserRepositoryAbstractClass):

    def get_all(self) -> List[User]:
        try:
            return self.conn.hgetall('user')
        except Exception as e:
            raise StorageException(e)

    def add(self, user: User) -> User:
        try:
            serialize = pickle.dumps(user)
            hash_ = hashlib.md5(str(user.__hash__()).encode()).hexdigest()
            user.id = hash_

            self.conn.hset(name='user', key=hash_, value=pickle.dumps(user), )
            return user
        except Exception as e:
            raise StorageException(e)

    def update(self, user: User) -> bool:
        try:
            self.conn.hset(
                name='user',
                key=user.id,
                value=pickle.dumps(user),
            )
            return user
        except Exception as e:
            raise StorageException(e)

    def delete(self, id: int) -> bool:
        try:
            result = self.conn.hdel('user', id)
            return True if result else False
        except Exception as e:
            raise StorageException(e)

    def get(self, id: int) -> User:
        try:
            result = self.conn.hget(name='user', key=id)
            return pickle.loads(result) if result else False
        except Exception as e:
            raise StorageException(e)


if __name__ == '__main__':
    user = User(
        first_name='ivan',
        middle_name='ivanovich',
        last_name='ivanov'
    )

    # postgres = Postgres(**DATABASES['postgres'])
    #
    # with PostgresUserRepository(postgres) as storage:
    #     user = storage.add(
    #         User(
    #             first_name='ivan',
    #             middle_name='ivanovich',
    #             last_name='ivanov'
    #         ),
    #     )
    #
    #     storage.complete()
    redis = Redis(**DATABASES['redis'])

    with RedisUserRepository(redis) as storage:
        print(storage.hkeys('user'))

        storage.execute()
