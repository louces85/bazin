import requests
from bs4 import BeautifulSoup
import re

class GoogleFinance:

    def getPriceStock(self, ticker):
        
        try:
            url = f'https://www.google.com/finance/quote/{ticker}:BVMF'
            
            response = requests.get(url)
            response.raise_for_status()  
            
            price_html = response.text.split("YMlKec fxKbKc")[1]
            soup = BeautifulSoup(price_html, "html.parser")
            
            
            price_text = soup.text
            price_match = re.search(r'(\d+\.\d+)', price_text)
            if price_match:
                price = price_match.group(0)
                return float(price)
            else:
                return "Value not found"

        except Exception as e:
            temp = ticker
            raise e