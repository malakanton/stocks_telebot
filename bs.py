#from os import name
import requests
import fake_useragent
from bs4 import BeautifulSoup

BASE_URL = 'https://www.marketbeat.com/stocks/NASDAQ/'
ua = fake_useragent.UserAgent()
headers = {'user_agent': ua.random}

BASE_URL = 'https://www.marketbeat.com/stocks/NASDAQ/'

class MarketBeatInfo():

    def __init__(self, ticker: str):
        self.ticker = ticker

    def _get_soup(self):
        url = BASE_URL + self.ticker + '/'
        result = requests.get(url, headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        return soup

    def get_analisys(self) -> list:
        analisys = []

        for item in self._get_soup().find('div', id='carouselRank') \
                .find('div', class_='carousel-item active rankAnalyst') \
                .find_all('p'):
            analisys.append(item.get_text())

        return '\n\n'.join(analisys)


