import requests
from io import StringIO
from datetime import datetime
from .exceptions import InvalidCurrency, RequestsError, InvalidYearException, InvalidFormatDate, DataNotFound
import pandas as pd
from enum import Enum

class Vars(Enum):
    """Global variables"""
    ENDPOINT = 'https://www.sbs.gob.pe/app/stats/seriesH-tipo_cambio_moneda_excel.asp'
    FORMAT   = '%d/%m/%Y'
    CURRENCIES = {
            'USD':'02'
        ,   'SEK':'55'
        ,   'CHF':'57'
        ,   'CAD':'11'
        ,   'EUR':'66'
        ,   'JPY':'38'
        ,   'GBP':'34'
    }

class SbsTC:
    """Exchange rate class"""
    
    def __init__(self,date_format='%d/%m/%Y'):
        """SbsTC base initializer

        Args:
            date_format (str, optional): Date format result. Defaults to '%d/%m/%Y'.
        """
        self.date_format = date_format
    
    def __get_currency(self,currency:str)->str:
        """Retrieves currency code

        Args:
            currency (str): Data currency

        Raises:
            InvalidCurrency: In case of an incorrect currency code

        Returns:
            str: Returns the currency code
        """
        try:
            return Vars.CURRENCIES.value[currency]
        except KeyError:
            raise InvalidCurrency(f'Invalid currency [{currency}]')
    
    def __get_request(self,parameters:dict)->StringIO:
        """Get data request

        Args:
            parameters (dict): Endpoint input parameters.

        Raises:
            RequestsError: In case of an error in the request

        Returns:
            StringIO: Request result converted into a StringIO object.
        """
        try:
            r = requests.get(
                    Vars.ENDPOINT.value
                ,   params=parameters
            )
            return StringIO(r.text)
        except Exception as e:
            raise RequestsError(str(e))
    
    @staticmethod
    def __valid_date(date:str)->bool:
        """Validating date

        Args:
            date (str): Date input

        Raises:
            InvalidYearException: In case of an error when the year of the input date is earlier than the year 2000
            InvalidFormatDate: In case of an error when the date format is incorrect

        Returns:
            bool: Return True when the format is correct.
        """
        try:
            date = datetime.strptime(date,'%d/%m/%Y')
            if date.year < 2000:
                raise InvalidYearException('Information avaible from the 2000 year')
            return True
        except Exception as e:
            raise InvalidFormatDate(str(e))
    
    def __get_data(self,currency:str,date:str,to_date:str)->dict:
        """Get exchange rate information and cleaning the data

        Args:
            currency (str): Currency code
            date (str): Start date
            to_date (str): End date

        Raises:
            DataNotFound: In case of not finding information

        Returns:
            dict: Exchange rate dictionary
        """
        
        self.__valid_date(date)
        self.__valid_date(to_date)
        
        from_date = datetime.strptime(date,'%d/%m/%Y')
        end_date  = datetime.strptime(to_date,'%d/%m/%Y')
        
        params = {
                "fecha1": from_date.strftime('%d/%m/%Y')
            ,   "fecha2": end_date.strftime('%d/%m/%Y')
            ,   "moneda": self.__get_currency(currency)
            ,   "cierre": ""
        }
        
        data_exchange = self.__get_request(params)
        dfs = pd.read_html(data_exchange, encoding='utf-8')
        
        if len(dfs[0]) <= 1:
            raise DataNotFound('There is no information available for the selected range')
        
        dfs[0].columns = dfs[0].iloc[0]
        dfs[0] = dfs[0][1:]
        df = dfs[0].drop('MONEDA', axis=1)
        if len(dfs[0])>0:
            data = df.to_dict(orient='dict')
        return data
        
    
    def get_exchange(self,currency:str,date:str,to_date:str=None)->dict:
        """Base function for obtaining the exchange rate

        Args:
            currency (str): Currency code
            date (str): Start Date
            to_date (str, optional): End Date. Defaults to None.

        Returns:
            dict: Formatted exchange rate dictionary
        """
        
        data = self.__get_data(currency,date,to_date or date)
        
        exchanges = []
        for key,value in data['FECHA'].items():
            
            fecha = datetime.strptime(value,Vars.FORMAT.value).strftime(self.date_format)
            exchange = {
                fecha:{
                    'buy':data['COMPRA'][key],
                    'sell':data['VENTA'][key]
                }
            }
            exchanges.append(exchange)
        final_data = {}
        for entry in exchanges:
            for date, rates in entry.items():
                final_data[date] = rates
        
        return final_data

if __name__ == '__main__':
    today = datetime.today()
    dias = datetime.timedelta(days=5)
    fec_ini = (today - dias).strftime('%d/%m/%Y')
    fec_fin = today.strftime('%d/%m/%Y')
    tc  = SbsTC(date_format='%Y-%m-%d')
    data = tc.get_exchange('USD',fec_fin)
    print(data)