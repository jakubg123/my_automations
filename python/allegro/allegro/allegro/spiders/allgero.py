import scrapy
from urllib.parse import quote
from ..items import AllegroItem

class AllegroSpider(scrapy.Spider):
    name = "allgero"

    def start_requests(self):
        url = "https://allegro.pl/listing?string=jedzenie%20dla%20ps%C3%B3w"
        yield scrapy.Request(url, meta={'playwright': True})

    async def parse(self, response):
        # for item in response.css('#search-results > div:nth-child(5) > div > div > div'):
         allegro_item = AllegroItem()
         allegro_item['text'] = response.xpath('//*[@id="search-results"]/div[5]/div/div/div/div/div/div/section[1]/article[1]/div/div[2]/div[1]/div/h2').get()
         yield allegro_item
