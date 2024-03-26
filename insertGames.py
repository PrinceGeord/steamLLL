from steamApiCalls import get_all_games, get_game_details
import psycopg2 as pg
from config import load_config

def insert_one_game(appid, name, genre):
    sql = """ INSERT INTO games(appid, name, genre)
                VALUES(%s, %s, %s) RETURNING *;"""
    data = (appid, name, genre)
    config = load_config()

    try:
        with pg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, data)
                conn .commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)


def insert_games(games):
    sql = "INSERT INTO games(appid, name) VALUES(%s, %s)"
    config = load_config()
    try:
        with pg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.executemany(sql, games)
                conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)

def insert_game_details(appid):
    deets = get_game_details(appid)
    config = load_config()
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
            with pg.connect(**config) as conn:
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
            with pg.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, [appid])
                    conn.commit()
                    return True
        except (Exception, pg.DatabaseError) as error:
            print(error)
            return False

def update_keywords_cache(p_keywords, n_keywords, appid):
    config=load_config()
    sql = """UPDATE games
            SET p_keywords = %s,
            n_keywords = %s
            WHERE appid = %s"""
    try:
        with pg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, [p_keywords, n_keywords, appid])
                conn.commit()
                return "keyword_cache_updated"
    except (Exception, pg.DatabaseError) as error:
        print(error)
        return 'keyword_cache update failed'




if __name__ == '__main__':
   print(update_keywords_cache('{"potato": 6, "tomato": 5}','{"orange": 4.3, "melon": 2.0}', 2357570))
