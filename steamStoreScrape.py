import requests
from bs4 import BeautifulSoup

def get_steam_genre_tags():
    url = 'http://store.steampowered.com/tag/browse/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    genre_tags = [tag.get('data-tagid') for tag in soup.findAll('div', class_='tag_browse_tag')]
    genre_names = [tag.text for tag in soup.findAll('div', class_='tag_browse_tag')]
    genre_dict = {}
    index = 0
    for tag in genre_tags:
            genre_dict[tag] = genre_names[index]
            index += 1
    print(genre_dict)

get_steam_genre_tags()
