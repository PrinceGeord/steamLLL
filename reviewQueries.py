from steamApiCalls import get_game_reviews
from datetime import date
import datetime
from config import load_config
import psycopg2 as pg

def insert_reviews(appid, page_limit=5):
    reviews = get_game_reviews(appid, page_limit)
    sql_review = """INSERT INTO reviews(recommendationid, appid, review, voted_up, timestamp_created, timestamp_updated) VALUES(%s, %s, %s, %s, %s, %s)
                ON CONFLICT (recommendationid) DO NOTHING"""
    sql_games = """UPDATE games SET last_review_request = %s WHERE appid = %s"""
    config = load_config() 
    form_reviews = []
    for review in reviews:
        form_review = {'recommendationid': int(review['recommendationid']), 'appid': appid, 'review': review['review'], 'voted_up': review['voted_up'], 'timestamp_created': datetime.datetime.fromtimestamp(review['timestamp_created']), 'timestamp_updated': datetime.datetime.fromtimestamp(review['timestamp_updated']) }
        form_reviews.append(list(form_review.values()))
    try:
        with pg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.executemany(sql_review, form_reviews)
                cur.execute(sql_games, [date.today(), appid ])
                conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)
    finally: print("Function ran - check database to confirm upload")

def fetch_reviews(appid, sentiment):
    config = load_config()
    sql = """SELECT review FROM reviews WHERE appid = %s AND voted_up = %s;"""
    try:
        with pg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, [appid, sentiment])
                raw_reviews = cur.fetchall()
                list_of_reviews = []
                for t in raw_reviews:
                    for item in t:
                        list_of_reviews.append(item)
                return list_of_reviews
    except (Exception, pg.DatabaseError) as error:
        print(error)


def get_last_review(appid):
    config = load_config()
    sql = """SELECT timestamp_updated:: DATE from reviews
WHERE appid = %s
ORDER BY timestamp_updated DESC
limit 1;;"""
    try:
        with pg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, [appid])
                return cur.fetchone()
    except (Exception, pg.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    print(get_last_review(20))