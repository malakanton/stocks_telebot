from yahoo_fin import stock_info as si

sp500 = set(si.tickers_sp500())
nasdaq = set(si.tickers_nasdaq())
dow = set(si.tickers_dow())
other = set(si.tickers_other())

tickers_list = set.union(sp500, nasdaq, dow, other)

with open('tickers_list.txt', 'w') as f:
    f.write(' '.join(tickers_list))
