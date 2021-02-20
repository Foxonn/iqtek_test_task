DATABASES = {
    'postgres_loc': {
        'dbname': 'usermanager',
        'user': 'postgres',
        'password': '185335',
        'host': 'localhost',
        'port': 5432,
    },
    'postgres': {
        'dbname': 'usermanager',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'postgres',
        'port': 5432,
    },
    'redis': {
        'db': 0,
        'host': 'redis',
        'port': 6379,
    },
    'mysql': {
        'db': 'usermanager',
        'user': 'mysql',
        'passwd': 'mysql',
        'host': 'mysql',
        'port': 3306,
    },
}

STORAGE = 'postgres'  # postgres, redis, mysql -> DATABASES[...]
