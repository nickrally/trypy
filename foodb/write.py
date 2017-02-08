import os, sys
import psycopg2
from psycopg2.extensions import AsIs
import yaml

# drop existing db with and re-create it before running this. See dropdb.py and createdb.py
with open('config.yml', 'r') as file:
    config = yaml.load(file)

USER = config['db']['user']
PASS = config['db']['password']
HOST = config['db']['host']
PORT = config['db']['port']

attributes = [
    {
        'name':'oid',
        'type':'bigint'
    },
    {
        'name':'name',
        'type':'text'
    },
    {
        'name':'fid',
        'type':'text'
    }]

def connect():
    db   = config['db']['name']
    user = config['db']['user']
    password = config['db']['password']
    host = config['db']['host']
    port = config['db']['port']

    try:
        db = psycopg2.connect(database=db, user=user,password=password, host=host,port=port)
        return db
    except psycopg2.Error as e:
        print("Unable to connect to db %s\n%s" %(db, e))


def create_table(cursor, table_name):
    try:
        cursor.execute("CREATE TABLE %s ();", (AsIs(table_name),))
    except psycopg2.Error as e:
        print("Unable to create table %s\n%s" % (table_name, e))
    except:
        print("Oh noes!")

def create_columns(cursor, table_name):
    try:
        for attr in attributes:
            cursor.execute("ALTER TABLE %s ADD COLUMN %s %s",(AsIs(table_name), AsIs(attr['name']), (AsIs(attr['type'])),))
    except psycopg2.Error as e:
        print("Unable to create column %s in table %s\n%s" %(attr['name'],table_name, e))


# def copy_to_db(cursor, table_name):
#     file_name = "%s.csv" % table_name
#     with open(file_name, 'r', newline='') as f:
#         sql = "COPY %s FROM '/%s/%s' DELIMITERS ',' CSV QUOTE '''';" % (table_name, os.getcwd(), file_name)
#         cursor.copy_expert(sql, f)
#     print("Inserted %s rows in %s table" % (cursor.rowcount, table_name))
#     cursor.execute("ALTER TABLE %s ADD PRIMARY KEY (oid);" % table_name)

def copy_to_db(cursor, table_name):
    file_name = "%s.csv" % table_name
    with open(file_name, 'r', newline='') as f:
        sql = cursor.mogrify("COPY %s FROM '/%s/%s' DELIMITERS ',';", (AsIs(table_name), AsIs(os.getcwd()), AsIs(file_name),))
        #cursor.copy_expert(sql=sql % (table_name, os.getcwd(), file_name), file=f)
        cursor.copy_expert(sql=sql, file=f)
    print("Inserted %s rows in %s table" % (cursor.rowcount, table_name))
    cursor.execute("ALTER TABLE %s ADD PRIMARY KEY (oid);" % table_name)

def run():
    db = connect()
    cursor = db.cursor()
    entities = config['db']['tables'].replace(',', ' ').split()
    for entity in entities:
        create_table(cursor, entity)
        create_columns(cursor, entity)
        copy_to_db(cursor, entity)

    db.commit()

run()

