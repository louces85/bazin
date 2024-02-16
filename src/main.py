import json
from model.valuation import Valuation
from model.google_finance import GoogleFinance
import threading
from prettytable import PrettyTable
import logging
from tqdm import tqdm
import datetime

LDM = 100000

myTable = PrettyTable(
    ["Ticker",
    "Preco Atual",
    "Valor Patrimonial",
    "Preco Teto",
    "Ganho",
    "Pontos MAX(13)",
    "Setor"]
)
myTable.align["Ticker"] = "l"

conditions = {
    'p_l': (lambda x: x < 0),
    'liquidezmediadiaria': (lambda x: x <= LDM),
}

def format_name(name,type,path):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d_%m_%Y_%H_%M_%S")
    file_name = f"{name}{formatted_time}{type}"
    file_path = f"{path}{file_name}"
    return file_path

def get_list_all_indicators(path_file):    
    with open(path_file, encoding='utf-8') as json_file:
        return json.load(json_file)

def save_results(table):
    with open(format_name("results_",".csv","src/results/"), 'w', newline='') as f_output:
        f_output.write(table.get_csv_string(delimiter=':'))

if __name__ == '__main__':

    logging.basicConfig(filename=format_name("log_",".log","src/logs/"), level=logging.INFO)

    list_all_indicators = get_list_all_indicators('src/files/all_indicators.json')

    for dictionary in tqdm(list_all_indicators, desc="progress"):
        try:

            if(not dictionary.get('p_l', None) or not dictionary.get('liquidezmediadiaria', None)):
                continue

            if any(condition(dictionary.get(indicator, None)) for indicator, condition in conditions.items()):
                continue

            ticker = dictionary['ticker']
            
            google_finance = GoogleFinance()

            def get_stock_price(ticker):
                global price_now
                price_now = google_finance.getPriceStock(ticker)

            price_now = None
            
            thread = threading.Thread(target=get_stock_price, args=(ticker,))
            thread.start()
            
            valuation = Valuation(ticker,'src/files/all_indicators.json')
            price_bazin = valuation.get_higher_price()

            thread.join()
            
            if(not price_bazin is None and not price_now is None):
                price_bazin = round(price_bazin,2)
                points_ticker = valuation.calculate_points_from_indicators()
                vpa_ticker = valuation.vpa
                ganho = round((price_bazin-price_now)*100/price_now,2)

                myTable.add_row(
                    [ticker,
                    price_now,
                    vpa_ticker,
                    price_bazin,
                    ganho,
                    points_ticker,
                    valuation.info]
                )
              
        except Exception as e:
            logging.exception(f"Error in ticker {ticker}: {e}")
            
    save_results(myTable)