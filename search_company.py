import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

SEARCH_URL = 'https://www.marketbeat.com/pages/search.aspx?query='

def search_word(search_txt):

    browser = webdriver.Chrome()
    browser.get(SEARCH_URL + search_txt)

    tickers = browser.find_elements(By.CLASS_NAME, 'ticker-area')
    titles = browser.find_elements(By.CLASS_NAME, 'title-area')

    results = [(ticker[0].text, ticker[1].text) for ticker in zip(tickers[:5], titles[:5])]

    browser.close()

    return results
