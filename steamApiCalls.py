import requests
import math
import numpy as np

def get_users_for_game(appid):
      url = f'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}'
      response = requests.get(url).json()
      print(response['response']['player_count'])

def get_all_games():
    response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/').json()
    raw_game_list = response['applist']['apps']
    game_dict = {}
    for game in raw_game_list:
        if game['name'] and game['appid'] not in game_dict:
                game_dict.update({game['appid']: game['name']})
        else:
            print("Exception: ", game)
    return list(game_dict.items())


def get_game_reviews(appid, page_limit=5):
    first_response = requests.get(f'https://store.steampowered.com/appreviews/{appid}?json=1&day_range=365&num_per_page=100&filter_offtopic_activity=0&filter=recent&language=english').json()
    total_reviews = first_response['query_summary']['total_reviews']
    review_pages = math.ceil(total_reviews /100)
    print("Total pages: ", review_pages)
    reviews = [first_response['reviews']]
    if review_pages == 1 or page_limit == 1:
        return np.array(reviews).flatten()
    cursor = first_response['cursor'].replace("+", "%2B")
    if review_pages < page_limit:
        page_limit = review_pages+1
    for i in range(1, page_limit):
        review_page_response = requests.get(f'https://store.steampowered.com/appreviews/{appid}?json=1&day_range=365&num_per_page=100&filter_offtopic_activity=0&filter=recent&language=english&cursor={cursor}').json()
        cursor = review_page_response['cursor'].replace("+", "%2B")
        if len(review_page_response['reviews']) > 0:
            reviews.append(review_page_response['reviews'])
        if i == page_limit:
            break
    print(len(reviews))
    return np.array(reviews).flatten()

def get_game_details(appid):
    response = requests.get(f'http://store.steampowered.com/api/appdetails/?appids={appid}&language=english').json()
    deets = {'type': None, 'genres': None, 'price_overview': {'initial': None}, 'short_description': None, 'capsule_imagev5': None, 'screenshots': [{'path_thumbnail': None}]}
    
    if response[str(appid)]['success']:
        for key in deets.keys():
            if key in response[str(appid)]['data']:
                deets[key] = response[str(appid)]['data'][key]
        game_dict = {'type': deets['type'], 'genres': deets['genres'], 'price': deets['price_overview']['initial'] ,'short_desc': deets['short_description'], 'thumbnail': deets['capsule_imagev5'], 'background': deets['screenshots'][0]['path_thumbnail'] }
        return game_dict
    else: return response[str(appid)]['success']


if __name__ == '__main__':
    print(get_game_reviews(2194810))