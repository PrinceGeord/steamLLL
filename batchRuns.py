from gameQueries import fetch_game_nulls
from insertGames import insert_game_details
from datetime import datetime
import time



def game_batch_details(limit = 5):
    hit_list = fetch_game_nulls()
    file_name = f'batchmisses_{datetime.now()}'
    missCount = 0
    api_calls = 0
    for hit in hit_list[:limit]:
        api_calls +=1
        if api_calls % 100 == 0:
            time.sleep(100)
        try:
            insert_game_details(hit)
        except:
            with open(file_name, "w") as f:
                f.write(str(hit) + "\n")
                missCount += 1
            if missCount == 10:
                break

    return f'{api_calls} apps have received updates, Errors: {missCount}'

    
if __name__ == "__main__":
    print(game_batch_details(3000))