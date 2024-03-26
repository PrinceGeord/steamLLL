from gameQueries import fetch_game_info
from insertGames import insert_game_details, update_keywords_cache
from datetime import date
from keyword_extract import get_keywords
import json
import queue

def load_game(appid):
     info = fetch_game_info(appid)
     if info[4] == None:
          insert_game_details(appid)
          info = fetch_game_info(appid)
     if info[9] == None or info[10] == None or info[8] < date.today():
          q = queue.Queue()
          q.put(get_keywords(appid, True).to_dict(orient='records'))
          q.put(get_keywords(appid, True).to_dict(orient='records'))
          p_raw = q.get()
          n_raw = q.get()
          p_keywords = {}
          n_keywords = {}
          for word in p_raw:
               p_keywords.update({word["keywords"]: word["score"]})
          for word in n_raw:
               n_keywords.update({word["keywords"]: word["score"]})
          update_keywords_cache(json.dumps(p_keywords), json.dumps(n_keywords), appid)

     else:
          # tidy this up later, "info" key should be reduced down to key information required to populate app
          p_keywords = info[9]
          n_keywords = info[10]
     print(n_keywords)
     return {'info': info, 'p_keywords': p_keywords, 'n_keywords': n_keywords }

if __name__ == "__main__":
     load_game(1336490)