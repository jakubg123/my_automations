import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional
import re

def get_links() -> list[str]:
    links = []

    for x in range(1, 6):
        req = requests.get(f'https://sklep-domwhisky.pl/pol_m_Scotch-Whisky_Blended-malt-whisky-205.html?counter={x - 1}')
        soup = BeautifulSoup(req.content, 'lxml')
        product_list = soup.find_all('div', class_="product_wrapper_sub")

        for item in product_list:
            for link in item.find_all('a', class_='product-name', href=True):
                links.append(link['href'])

    return links

def parse_whisky(link: str) -> dict:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')

    name = soup.find('h1', itemprop='name').text.strip()
    price_element = soup.find('strong', class_='projector_price_value')
    price_text = price_element.text.strip()
    price = re.sub(r'\s*zł\s*', '', price_text)  # Non-converted from 121,41 zl for training purpose
    try:
        rating = soup.find('small', itemprop='ratingValue').text.strip()
    except:
        rating = 'no rating available'
    reviews = soup.find_all('span', itemprop='description')

    review_list = [f'{review.text}' for review in reviews]
    reviews_amount = len(review_list)

    whisky = {
        'name': name,
        'price': price,
        'rating': rating,
        'reviews_amount': reviews_amount,
        'reviews': review_list
    }

    return whisky

def main():
    links = get_links()

    whisky_list = []
    for link in links:
        whisky = parse_whisky(link)
        whisky_list.append(whisky)

    df = pd.DataFrame(whisky_list)
    df.to_csv("whisky.csv")

if __name__ == "__main__":
    main()