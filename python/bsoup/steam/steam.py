import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from typing import Optional

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1'


def get_steam_games(steam_url) -> int:
    req = requests.get(steam_url)
    data = dict(req.json())
    all_requests = data['total_count']
    return int(all_requests)


def get_data(steam_url):
    req = requests.get(url)
    data = dict(req.json())
    return data['results_html']


def parse(data: str) -> list[dict]:
    game_list = []
    soup = BeautifulSoup(data, "html.parser")
    games = soup.find_all('a')

    for game in games:
        title = game.find('span', 'title').text.strip()

        price_elem = game.find('div', 'discount_original_price')
        price: Optional[float] = None
        if price_elem is not None:
            price_text = price_elem.text.strip().split(" ")[0].replace(',', '.')
            price = float(price_text)

        discount_elem = game.find('div', 'discount_final_price')
        discount_price: Optional[float] = None
        if discount_elem is not None:
            discount_text = discount_elem.text.strip().split(" ")[0].replace(',', '.')
            if discount_text.lower() == 'free':
                discount_price = 0.0
            else:
                discount_price = float(discount_text)
        discount_percentage = 0

        if discount_price is not None and price is not None:
            discount_percentage = round((discount_price / price) * 100)

        steam_game = {
            'title': title,
            'price': price,
            'discount_price': discount_price,
            'discount_percentage': discount_percentage
        }

        game_list.append(steam_game)

    return game_list


def generateDF(game_list) -> None:
    game_list_df = pd.concat([pd.DataFrame(g) for g in game_list])
    game_list_df.to_csv("steam.csv", index=False)


res = []
for i in range(0, get_steam_games(url), 50):
    data = get_data(
        f'https://store.steampowered.com/search/results/?query&start=0&count={i}&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1')
    res = parse(data)

generateDF(res)
