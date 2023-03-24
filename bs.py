#from os import name
import requests
import fake_useragent
from bs4 import BeautifulSoup
import re

BASE_URL = 'https://www.marketbeat.com/stocks/NASDAQ/'
ua = fake_useragent.UserAgent()
headers = {'user_agent': ua.random}

BASE_URL = 'https://www.marketbeat.com/stocks/NASDAQ/'

class MarketBeatInfo():

    def __init__(self, ticker: str):
        self.ticker = ticker

    def get_name(self)-> str:
        title = self._get_soup().find('h1', class_='PageTitleHOne').get_text()
        return re.sub(r'\n', '', re.split(r'Stock', title)[0])

    def _get_soup(self):
        url = BASE_URL + self.ticker + '/'
        result = requests.get(url, headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        return soup

    def get_analysis(self) -> str:
        analysis = []

        for item in self._get_soup().find('div', id='carouselRank') \
                .find('div', class_='carousel-item active rankAnalyst') \
                .find_all('p'):
            analysis.append(item.get_text())

        return '\n\n'.join(analisys)

    def get_sustainability(self)-> str:
        sustainability = []
        for item in self._get_soup().find('div', id='carouselRank') \
                .find('div', class_='carousel-item rankSustainability') \
                .find_all('li'):
            sustainability.append(item.get_text())
        return '\n\n'.join(sustainability)

