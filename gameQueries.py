import psycopg2 as pg
import streamlit as st


def fetch_game_name(appid):
    sql = """SELECT game_name FROM games WHERE appid = %s;"""
    try:
        with pg.connect(st.secrets["postgresql"]) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, [appid])
                raw_name = cur.fetchone()
                return raw_name[0]
    except (Exception, pg.DatabaseError) as error:
        print(error)

def fetch_game_nulls():
    sql = """SELECT appid FROM games WHERE app_type IS NULL"""
    try:
        with pg.connect(st.secrets["postgresql"]) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                raw_list = cur.fetchall()
                form_list = [i[0] for i in raw_list]
                form_list.sort()
                return form_list
    except(Exception, pg.DatabaseError) as error:
        print(error)

def fetch_games():
    sql = """SELECT appid, game_name, thumbnail FROM games
            WHERE app_type = 'game' OR app_type IS NULL"""
    try:
        with pg.connect(st.secrets["postgresql"]) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
    except(Exception, pg.DatabaseError) as error:
        print(error)


def fetch_game_info(appid):
    sql = """SELECT * FROM games
            WHERE appid = %s"""
    try:
        with pg.connect(st.secrets["postgresql"]) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, [appid] )
                return cur.fetchone()
    except(Exception, pg.DatabaseError) as error:
        print((error))

if __name__ == "__main__":
    print(fetch_game_info(1336490))
