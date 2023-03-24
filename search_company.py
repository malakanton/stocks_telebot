import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

SEARCH_URL = 'https://www.marketbeat.com/pages/search.aspx?query='

with open('tickers_list.txt', 'r') as f:
    tickers_list = f.readline().split()

def search_word(search_txt):

    browser = webdriver.Chrome()
    browser.get(SEARCH_URL + search_txt)

    tickers = browser.find_elements(By.CLASS_NAME, 'ticker-area')
    titles = browser.find_elements(By.CLASS_NAME, 'title-area')

    results = [(t[0].text, t[1].text) for t in zip(tickers[:10], titles[:10]) if t[0].text in tickers_list]

    browser.close()

    return '\n'.join([f'<b>{t[0]}</b> -> {t[1]}' for t in results])
