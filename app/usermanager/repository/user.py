from typing import List, Union
from abc import ABCMeta, abstractmethod
import pickle

import hashlib

from app.usermanager.entities.user import User
from app.usermanager.storage.exceptions import StorageException, ItemNotFound
from app.usermanager.storage import (
    SQLStorage,
    RedisStorage,
    Redis,
    Postgres,
    MySQL,
)
from app.usermanager.settings import DATABASES


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


class MySQLUserRepository(SQLStorage, UserRepositoryAbstractClass):
    def __init__(self, *args, **kwargs):
        if not isinstance(args[0], MySQL):
            raise TypeError('Type error, "storage" is not MySQL')

        super(MySQLUserRepository, self).__init__(*args, **kwargs)

    def get_all(self) -> List[User]:
        c = self.conn.cursor()

        query = "SELECT * FROM users;"

        c.execute(query)

        rows = c.fetchall()

        if not rows:
            return []

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

    def add(self, user: User) -> User:
        c = self.conn.cursor()

        query = """
                INSERT INTO users (first_name, middle_name, last_name)
                VALUES('{first_name}', '{middle_name}', '{last_name}');
            """.format(
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
        )

        c.execute(query)

        c.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1;")

        user.id = c.fetchone()[0]

        return user

    def get(self, id: int) -> Union[User, bool]:
        c = self.conn.cursor()

        query = "SELECT * FROM users WHERE id={id};".format(id=id)

        c.execute(query)

        row = c.fetchone()

        if not row:
            raise ItemNotFound(f'User id={id} not found!')

        id, first_name, middle_name, last_name = row

        user = User(
            id=id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
        )

        return user

    def delete(self, id: int) -> bool:
        c = self.conn.cursor()

        query = "DELETE FROM users WHERE id={id};".format(id=id)

        c.execute(query)

        if c.rowcount:
            return True
        raise ItemNotFound(f'User id={user.id} not found!')

    def update(self, user: User) -> bool:
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
        raise ItemNotFound(f'User id={user.id} not found!')


class PostgresUserRepository(SQLStorage, UserRepositoryAbstractClass):
    def __init__(self, *args, **kwargs):
        if not isinstance(args[0], Postgres):
            raise TypeError('Type error, "storage" is not Postgres')

        super(PostgresUserRepository, self).__init__(*args, **kwargs)

    def get_all(self) -> List[User]:

        c = self.conn.cursor()

        query = "SELECT * FROM users;"

        c.execute(query)

        rows = c.fetchall()

        if not rows:
            return []

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

    def add(self, user: User) -> User:
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

    def get(self, id: int) -> Union[User, bool]:
        c = self.conn.cursor()

        query = "SELECT * FROM users WHERE id={id};".format(id=id)

        c.execute(query)

        row = c.fetchone()

        if not row:
            raise ItemNotFound(f'User id={id} not found!')

        id, first_name, middle_name, last_name = row

        user = User(
            id=id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
        )

        return user

    def delete(self, id: int) -> bool:
        c = self.conn.cursor()

        query = "DELETE FROM users WHERE id={id};".format(id=id)

        c.execute(query)

        if c.rowcount:
            return True

        raise ItemNotFound(f'User id={user.id} not found!')

    def update(self, user: User) -> bool:
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

        raise ItemNotFound(f'User id={user.id} not found!')


class RedisUserRepository(RedisStorage, UserRepositoryAbstractClass):

    def __init__(self, *args, **kwargs):
        if not isinstance(args[0], Redis):
            raise TypeError('Type error, "storage" is not Redis')

        super(RedisUserRepository, self).__init__(*args, **kwargs)

    def get_all(self) -> List[User]:
        all = self.conn.hgetall('user')
        users = []

        if not all:
            return []

        for user in all.values():
            users.append(pickle.loads(user))

        return users

    def add(self, user: User) -> User:
        serialize = pickle.dumps(user)
        hash_ = hashlib.md5(str(user.__hash__()).encode()).hexdigest()
        user.id = hash_

        self.conn.hset(name='user', key=hash_, value=pickle.dumps(user), )
        return user

    def update(self, user: User) -> bool:
        self.conn.hset(
            name='user',
            key=user.id,
            value=pickle.dumps(user),
        )
        return user

    def delete(self, id: int) -> bool:
        result = self.conn.hdel('user', id)
        return True if result else False

    def get(self, id: int) -> User:
        result = self.conn.hget(name='user', key=id)

        if not result:
            raise ItemNotFound(f'User id={id} not found!')

        user = pickle.loads(result)

        return user if result else False


if __name__ == '__main__':
    user = User(
        first_name='ivan',
        middle_name='ivanovich',
        last_name='ivanov'
    )

    storage = Redis(**DATABASES['redis'])

    with RedisUserRepository(storage) as rep:
        print(user)
        user_ = rep.add(user)
        print(rep.get(user_.id))
        users = rep.get_all()
        print(users)
        rep.execute()
