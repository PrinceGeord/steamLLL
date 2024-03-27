from gameQueries import fetch_game_info
from insertGames import insert_game_details, update_keywords_cache
from datetime import date
from keyword_extract import get_keywords
import json

def load_game(appid):
     info = fetch_game_info(appid)
     if info[3] == None:
          insert_game_details(appid)
          info = fetch_game_info(appid)
     if info[3] != "game":
          return {'info': info}
     if info[9] == None or info[10] == None or info[8] < date.today():
          keywords = get_keywords(appid)
          if isinstance(keywords, str):
               return {'info': info}
          p_raw = keywords[0].to_dict(orient='records')
          n_raw = keywords[1].to_dict(orient='records')
          p_keywords = {}
          n_keywords = {}
          for word in p_raw:
               p_keywords.update({word["keywords"]: word["score"]})
          for word in n_raw:
               n_keywords.update({word["keywords"]: word["score"]})
          update_keywords_cache(json.dumps(p_keywords), json.dumps(n_keywords), appid)
     else:
          p_keywords = info[9]
          n_keywords = info[10]
     return {'info': info, 'p_keywords': p_keywords, 'n_keywords': n_keywords }

if __name__ == "__main__":
     load_game(1336490)