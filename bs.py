import requests
import fake_useragent
from bs4 import BeautifulSoup
import re

BASE_URL = 'https://www.marketbeat.com/stocks/NASDAQ/'
ua = fake_useragent.UserAgent()
headers = {'user_agent': ua.random}


class MarketBeatInfo:

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.soup = self._get_soup()

    def _get_soup(self, section: str = ''):
        url = BASE_URL + self.ticker + f'/{section}'
        result = requests.get(url, headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        return soup

    def get_name(self) -> str:
        title = self.soup.find('h1', class_='PageTitleHOne').get_text()
        return re.sub(r'\n', '', re.split(r'Stock', title)[0])

    def get_about(self) -> list:
        about = []
        for item in self.soup.find('div', class_="read-more-section") \
                             .find_all('p'):
            about.append(item.get_text())
        return '\n\n'.join(about)

    def get_analysis(self) -> str:
        analysis = []

        for item in self.soup.find('div', id='carouselRank') \
                        .find('div', class_='carousel-item active rankAnalyst') \
                        .find_all('p'):
            analysis.append(item.get_text())
        lst = analysis[0].split()
        lst.insert(lst.index('of') + 1, '<b>')
        lst.insert(lst.index('The'), '</b>\n')
        analysis[0] = ' '.join(lst)
        return '\n\n'.join(analysis)

    def get_sustainability(self) -> str:
        sustainability = []
        for item in self.soup.find('div', id='carouselRank') \
                        .find('div', class_='carousel-item rankSustainability') \
                        .find_all('li'):
            item = re.sub(r'Overall ESG \(Environmental, Social, and Governance\) Score',
                          'Overall ESG (Environmental, Social, and Governance) Score:\n', item.get_text())
            item = re.sub(r'Environmental Sustainability',
                          'Environmental Sustainability:\n', item)
            sustainability.append(item)
        return '\n\n'.join(sustainability)

    def get_dividend(self) -> str:
        dividend = []
        for item in self.soup.find('div', id='carouselRank') \
                        .find('div', class_='carousel-item rankDividend') \
                        .find_all('li'):
            item = re.sub(r'Dividend Yield|Dividend Growth|Dividend Coverage|Dividend Sustainability', '',
                          item.get_text())
            dividend.append(item)
        return '\n\n'.join(dividend)

    def get_chart(self) -> str:
        text = self.soup.find('div', class_='h3 m-0 pt-3 d-inline-block').get_text()
        text_div = text.split(':')
        market, ticker = text_div[0], text_div[1]
        return f'https://www.tradingview.com/symbols/{market}-{ticker}/'
