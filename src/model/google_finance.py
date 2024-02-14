import requests
from bs4 import BeautifulSoup
import re
import time

class GoogleFinance:

    def getPriceStock(self, ticker):
        
        try:
            url = f'https://www.google.com/finance/quote/{ticker}:BVMF'
            
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for any bad response status
            
            # Create a BeautifulSoup object only for the required part of the HTML
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

# start_time = time.time()
# test = GoogleFinance()
# print(test.getPriceStock("ITUB4"))
# end_time = time.time()  # Registra o tempo de fim
# execution_time = end_time - start_time
# print(f"Tempo de execução: {execution_time} segundos")