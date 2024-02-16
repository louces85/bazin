import requests
from bs4 import BeautifulSoup
import re

class GoogleFinance:

    def getPriceStock(self, ticker):
        try:
            url = f'https://www.google.com/finance/quote/{ticker}:BVMF'
            
            response = requests.get(url)
            response.raise_for_status()  
            
            price_html = response.text.split("YMlKec fxKbKc")
            if len(price_html) > 1:
                price_html = price_html[1]
            else:
                return None
            
            soup = BeautifulSoup(price_html, "html.parser")
            price_text = soup.text
            price_match = re.search(r'(\d+\.\d+)', price_text)
            if price_match:
                price = price_match.group(0)
                return float(price)
            else:
                return None

        except Exception as e:
            raise e