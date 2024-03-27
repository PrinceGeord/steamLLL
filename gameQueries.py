from config import load_config
import psycopg2 as pg
import time


def fetch_game_name(appid):
    config = load_config()
    sql = """SELECT game_name FROM games WHERE appid = %s;"""
    try:
        with pg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, [appid])
                raw_name = cur.fetchone()
                return raw_name[0]
    except (Exception, pg.DatabaseError) as error:
        print(error)

def fetch_game_nulls():
    config = load_config()
    sql = """SELECT appid FROM games WHERE app_type IS NULL"""
    try:
        with pg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                raw_list = cur.fetchall()
                form_list = [i[0] for i in raw_list]
                form_list.sort()
                return form_list
    except(Exception, pg.DatabaseError) as error:
        print(error)

def fetch_games():
    config = load_config()
    sql = """SELECT appid, game_name, thumbnail FROM games
            WHERE app_type = 'game' OR app_type IS NULL"""
    try:
        with pg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
    except(Exception, pg.DatabaseError) as error:
        print(error)


def fetch_game_info(appid):
    config = load_config()
    sql = """SELECT * FROM games
            WHERE appid = %s"""
    try:
        with pg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, [appid] )
                return cur.fetchone()
    except(Exception, pg.DatabaseError) as error:
        print((error))

if __name__ == "__main__":
    print(fetch_games())
