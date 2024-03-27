from steamApiCalls import get_all_games, get_game_details
import psycopg2 as pg
import os

def insert_one_game(appid, name, genre):
    sql = """ INSERT INTO games(appid, name, genre)
                VALUES(%s, %s, %s) RETURNING *;"""
    data = (appid, name, genre)

    try:
        with pg.connect(dbname="pagila",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host="data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com",
            port="5432") as conn:
            with conn.cursor() as cur:
                cur.execute(sql, data)
                conn .commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)


def insert_games(games):
    sql = """INSERT INTO games(appid, game_name) VALUES(%s, %s)
    ON CONFLICT (appid) DO NOTHING"""
    try:
        with pg.connect(dbname="pagila",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host="data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com",
            port="5432") as conn:
            with conn.cursor() as cur:
                cur.executemany(sql, games)
                conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)

def insert_game_details(appid):
    deets = get_game_details(appid)
    if deets:
        if deets['genres']:
            if len(deets['genres']) > 2:
                genre_lim = 2
            else: genre_lim = len(deets['genres'])
            genres = ", ".join([genre['description'] for genre in deets['genres'][:genre_lim]])
        else: genres = None
        sql = """ UPDATE games
        SET app_type = %s,
        genre = %s, 
        price = %s, 
        short_desc = %s,
        thumbnail = %s,
        background = %s
        WHERE appid = %s;"""
        deetsList = [deets['type'], genres, deets['price'], deets['short_desc'], deets['thumbnail'], deets['background'], appid]
        try:
            with pg.connect(dbname="pagila",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host="data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com",
            port="5432") as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, deetsList)
                    conn.commit()
                    return True
        except (Exception, pg.DatabaseError) as error:
            print(error)
            return False
    else: 
        sql = """UPDATE games SET app_type = 'config' WHERE appid = %s"""
        try:
            with pg.connect(dbname="pagila",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host="data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com",
            port="5432") as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, [appid])
                    conn.commit()
                    return True
        except (Exception, pg.DatabaseError) as error:
            print(error)
            return False

def update_keywords_cache(p_keywords, n_keywords, appid):
    sql = """UPDATE games
            SET p_keywords = %s,
            n_keywords = %s
            WHERE appid = %s"""
    try:
        with pg.connect(dbname="pagila",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host="data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com",
            port="5432") as conn:
            with conn.cursor() as cur:
                cur.execute(sql, [p_keywords, n_keywords, appid])
                conn.commit()
                return "keyword_cache_updated"
    except (Exception, pg.DatabaseError) as error:
        print(error)
        return 'keyword_cache update failed'

if __name__ == '__main__':
   insert_games(get_all_games())
