from steamApiCalls import get_all_games

def get_dupe_games(list):

    d = {}

    duplicates = []

    for tup in list:
        if tup in d:
            duplicates.append(tup)
        else:
            d[tup] = 1

    return duplicates

def check_id(appid):
    list = get_all_games()

    print([item for item in list if item[0] == appid])



if __name__ == "__main__":
    #print(get_dupe_games(get_all_games()))
    check_id(2100400)