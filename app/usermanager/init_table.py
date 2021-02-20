from settings import DATABASES
from storage import Postgres, MySQL


def create_table(storage):
    query = """ 
        CREATE TABLE users (
             id serial,
             first_name varchar(50),
             middle_name varchar(50),
             last_name varchar(50) 
         ); 
    """
    conn = storage.get_connection()
    cur = conn.cursor()

    cur.execute(query)

    conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    postgres_conn = Postgres(**DATABASES.get('postgres'))
    mysql_conn = MySQL(**DATABASES.get('mysql'))

    create_table(postgres_conn)
    create_table(mysql_conn)
