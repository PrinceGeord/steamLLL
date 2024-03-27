import psycopg2
import os

def connect():
    """ Connect to the postgres database server"""
    try:
        #connecting to the postgres server
        with psycopg2.connect(
            dbname="pagila",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host="data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com",
            port="5432"
        ) as conn:
            print('Connected to the PostgreSQL server')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    connect()