import psycopg2
import os

def create_tables():
    commands = (
        """
    CREATE TABLE games (
    appid INTEGER PRIMARY KEY,
    game_name VARCHAR(300),
    genre VARCHAR(60),
    app_type VARCHAR(20),
    price INTEGER,
    short_desc TEXT,
    thumbnail TEXT,
    background TEXT,
    last_review_request DATE,
    p_keywords JSON,
    n_keywords JSON
    )
""",
""" CREATE TABLE reviews (
    recommendationid INTEGER PRIMARY KEY,
    appid INTEGER,
    FOREIGN KEY (appid)
        REFERENCES games (appid)
        ON UPDATE CASCADE ON DELETE CASCADE,
    review VARCHAR(8000),
    voted_up boolean,
    timestamp_created TIMESTAMP,
    timestamp_updated TIMESTAMP
)"""
    )
    try:
        with psycopg2.connect(dbname="pagila",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host="data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com",
            port="5432") as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
if __name__ == '__main__':
    create_tables()
