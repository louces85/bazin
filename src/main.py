import json
from model.valuation import Valuation
from model.google_finance import GoogleFinance
import threading
from prettytable import PrettyTable
import logging
from tqdm import tqdm
import time
import csv
import datetime

if __name__ == '__main__':

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d_%m_%Y_%H_%M_%S")
    file_name = f"log_{formatted_time}.log"
    file_path = f"src/logs/{file_name}"

    logging.basicConfig(filename=file_path, level=logging.INFO)

    list_all_indicators = []

    with open('src/files/all_indicators.json', encoding='utf-8') as json_file:
        list_all_indicators = json.load(json_file)

    myTable = PrettyTable(["Ticker","Preco Atual","Valor Patrimonial","Preco Teto","Ganho","Pontos MAX(13)","Setor"])
    myTable.align["Ticker"] = "l"
    
    for dict in tqdm(list_all_indicators, desc="Progresso"):
        try:
            if( dict['p_l'] <= 0):
                continue
            
            if 'liquidezmediadiaria' in dict and dict['liquidezmediadiaria'] <= 100000:
                    continue
            
            if not 'liquidezmediadiaria' in dict:
                    continue
                    
            ticker = dict['ticker']
            
            google_finance = GoogleFinance()

            def get_stock_price(ticker):
                global price_now
                price_now = google_finance.getPriceStock(ticker)

            price_now = None
            
            thread = threading.Thread(target=get_stock_price, args=(ticker,))
            thread.start()
            
            valuation = Valuation(ticker,'src/files/all_indicators.json')
            price_basin = valuation.get_higher_price()

            thread.join()
            
            if(not price_basin is None):
                price_basin = round(price_basin,2)
                points_ticker = valuation.calculate_points_from_indicators()
                vpa_ticker = valuation.vpa
                ganho = round((price_basin-price_now)*100/price_now,2)

                myTable.add_row([ticker,price_now,vpa_ticker,price_basin,ganho,points_ticker,valuation.info])
                #print(f'{ticker}:{price_now}:{vpa_ticker}:{price_basin}:{points_ticker}:{valuation.info}')
                 
        except Exception as e:
            logging.exception(f"Error: {e}")
    

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d_%m_%Y_%H_%M_%S")
    file_name = f"results_{formatted_time}.csv"
    file_path = f"src/results/{file_name}"
    
    with open(file_path, 'w', newline='') as f_output:
        f_output.write(myTable.get_csv_string(delimiter=':'))