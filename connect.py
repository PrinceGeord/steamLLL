import psycopg2
import streamlit as st

def connect():
    """ Connect to the postgres database server"""
    try:
        #connecting to the postgres server
        with psycopg2.connect(st.secrets['postgresql']) as conn:
            print('Connected to the PostgreSQL server')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    connect()