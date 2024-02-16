from re import S
from .dividends import Dividends
import datetime
from dateutil.relativedelta import relativedelta
import json
import sys
import os
sys.path.append(os.path.realpath('.'))
from enums.rules import Rules

class Valuation:

    def __init__(self, ticker, json_file_path):
        
        self._ticker = ticker
        self._dividends = Dividends(self._ticker)
        self._json_file_path = json_file_path
        self.vpa = None
        self.info = "-"

    def get_higher_price(self):

        list_div = self._dividends.get_all_dividens_by_year()

        if(not list_div):
            return None

        sum_of_div = 0
        numbers_of_years = 0
        
        for year in self.get_past_years(5):

            value_year = self.search_value_by_year(list_div,int(year))
            
            if(value_year):
                sum_of_div+=value_year
                numbers_of_years+=1
        
        try:
            avg = sum_of_div/numbers_of_years
        except Exception as e:
            return None
        
        higher_price = avg/Rules.BAZIN.value
        return higher_price
            
    def search_value_by_year(self,list_of_dictionary, year):
        return next((dicionario.get('sum') for dicionario in list_of_dictionary if dicionario.get('year') == year), None)
    
    def get_past_years(self,number_of_years):
        return [(datetime.datetime.now() - relativedelta(years=i)).strftime("%Y") for i in range(1, number_of_years + 1)]
    
    def get_indicators_from_json_file(self):
        
        list_all_indicators = []

        with open(self._json_file_path, encoding='utf-8') as json_file:
            list_all_indicators = json.load(json_file)

        return next((dicionario for dicionario in list_all_indicators if dicionario.get('ticker') == self._ticker), None)

    def calculate_points_from_indicators(self):
        
        dictionary = self.get_indicators_from_json_file()
        self.vpa = dictionary['vpa']
        self.info = dictionary.get('segmentname','-')
        
        points = 0

        indicators_conditions = {
            'p_l': (lambda x: x < Rules.P_L.value),
            'dy': (lambda x: x >= Rules.D_Y.value),
            'p_vp': (lambda x: x <= Rules.P_VP.value),
            'dividaliquidapatrimonioliquido': (lambda x: x <= Rules.DL_PL.value),
            'dividaliquidaebit': (lambda x: x <= Rules.DL_EBITDA.value),
            'passivo_ativo': (lambda x: x <= Rules.P_A.value),
            'liquidezcorrente': (lambda x: x >= Rules.L_Q.value),
            'margemebit': (lambda x: x >= Rules.M_EBIT.value),
            'margemliquida': (lambda x: x >= Rules.M_L.value),
            'roe': (lambda x: x >= Rules.ROE.value),
            'roic': (lambda x: x >= Rules.ROIC.value),
            'receitas_cagr5': (lambda x: x >= Rules.CAGR_R.value),
            'lucros_cagr5': (lambda x: x >= Rules.CAGR_L.value)
        }

        for indicator, condition in indicators_conditions.items():
            if indicator in dictionary and condition(dictionary[indicator]):
                points += 1
        
        return points