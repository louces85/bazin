from mimetypes import init
from tkinter import N
import yfinance
import pandas as pd

class Dividends():

    def __init__(self,ticker):
        
        self._ticker = ticker
        self._msft = None
        self._list_sum_div_by_year = []
        self._history_dividends = None

    def get_all_dividens_by_year(self):

        msft = yfinance.Ticker(f'{self._ticker}.SA')
        self._msft = msft
        #tmp = msft.splits
        #print(tmp)
        history_dividends = msft.dividends
        self._history_dividends = history_dividends        
        
        if isinstance(history_dividends, list):
            return self._list_sum_div_by_year

        history_dividends.index = pd.to_datetime(history_dividends.index)
        sum_by_year = history_dividends.groupby(history_dividends.index.year).sum()
        self._list_sum_div_by_year = [{'year': year, 'sum': sum} for year, sum in sum_by_year.items()]
        
        return self._list_sum_div_by_year[::-1]