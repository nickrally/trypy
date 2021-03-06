import psycopg2
import yaml

'''
to check outcomes in terminal:
    $ sudo su postgres
    bash-3.2$ psql -l


########  config example:
db:
    name: foobar
    user: postgres
    password: postgres
    host: 127.0.0.1
    port: 5432
    tables: foo, bar
'''



with open('config.yml', 'r') as file:
    config = yaml.load(file)

USER = config['db']['user']
PASS = config['db']['password']
HOST = config['db']['host']
PORT = config['db']['port']


def create_db(dbname):
    with psycopg2.connect(database="postgres", user=USER, password=PASS, host=HOST, port=PORT) as conn:
        with conn.cursor() as cur:
            # use set_isolation_level(0) to avoid psycopg2.InternalError: CREATE DATABASE cannot run inside a transaction block
            conn.set_isolation_level(0)
            cur.execute('CREATE DATABASE ' + dbname)
            cur.close()
    return True

def test_create_db():
    dbname = config["db"]["name"]
    result = False
    try:
        result = create_db(dbname)
    except psycopg2.Error as e:
        print ("oh noes! " + e.pgerror)
    else:
        print ("great success!")
    assert result