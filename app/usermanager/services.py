from app.usermanager.settings import STORAGE
from app.usermanager.storage import Redis, Postgres
from app.usermanager.entities.user import User
from app.usermanager.settings import DATABASES, STORAGE
from app.usermanager.repository import (
    RedisUserRepository,
    PostgresUserRepository,
    MySQLUserRepository,
    Redis,
    Postgres,
    MySQL,
)


def get_conn_repository(db: str):
    if db == 'postgres':
        conn = Postgres(**DATABASES.get('postgres'))
        repository = PostgresUserRepository(conn)
        return repository

    if db == 'mysql':
        conn = MySQL(**DATABASES.get('mysql'))
        repository = MySQLUserRepository(conn)
        return repository

    if db == 'redis':
        conn = Redis(**DATABASES.get('redis'))
        repository = RedisUserRepository(conn)
        return repository

    raise Exception('Database settings not found.')


def add_user(user_):
    repository = get_conn_repository(STORAGE)

    with repository as rep:
        entity_user = rep.add(
            User(
                first_name=user_.first_name,
                middle_name=user_.middle_name,
                last_name=user_.last_name,
            )
        )

        rep.execute()

    user = {
        'id': entity_user.id,
        'first_name': entity_user.first_name,
        'middle_name': entity_user.middle_name,
        'last_name': entity_user.last_name,
    }

    return user


def get_all_users():
    repository = get_conn_repository(STORAGE)

    with repository as repos:
        entities_users = repos.get_all()

    users = []

    for user in entities_users:
        users.append(
            {
                'id': user.id,
                'first_name': user.first_name,
                'middle_name': user.middle_name,
                'last_name': user.last_name,
            }
        )

    return users


def delete_user(id: int):
    repository = get_conn_repository(STORAGE)

    with repository as repos:
        entity_user = repos.get(id)
        result = repos.delete(entity_user.id)
        repos.execute()

    return result


def get_user_by_id(id: int):
    repository = get_conn_repository(STORAGE)

    with repository as repos:
        entity_user = repos.get(id)

    user = {
        'id': entity_user.id,
        'first_name': entity_user.first_name,
        'middle_name': entity_user.middle_name,
        'last_name': entity_user.last_name,
    }

    return user


def update_user(id, user):
    repository = get_conn_repository(STORAGE)

    with repository as repos:
        entity_user = repos.get(id)

        entity_user.first_name = user.first_name
        entity_user.middle_name = user.middle_name
        entity_user.last_name = user.last_name

        repos.update(entity_user)
        repos.execute()

    user = {
        'id': entity_user.id,
        'first_name': entity_user.first_name,
        'middle_name': entity_user.middle_name,
        'last_name': entity_user.last_name,
    }

    return user


def partial_update_user(id, user):
    repository = get_conn_repository(STORAGE)

    with repository as repos:
        entity_user = repos.get(id)

        if user.first_name:
            entity_user.first_name = user.first_name

        if user.middle_name:
            entity_user.middle_name = user.middle_name

        if user.last_name:
            entity_user.last_name = user.last_name

        repos.update(entity_user)
        repos.execute()

    user = {
        'id': entity_user.id,
        'first_name': entity_user.first_name,
        'middle_name': entity_user.middle_name,
        'last_name': entity_user.last_name,
    }

    return user
