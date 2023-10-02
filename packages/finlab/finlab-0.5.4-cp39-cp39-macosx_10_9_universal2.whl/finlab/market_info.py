import logging
import pandas as pd
from typing import Dict, Optional, Union

import finlab.data

class MarketInfo():
    """市場類別
    假如希望開發新的交易市場套用到回測系統，可以繼承 `finlab.market_info.MarketInfo` 來實做新類別。
    """
    @staticmethod
    def get_freq() -> str:
        return '1d'

    @staticmethod
    def get_name() -> str:
        return 'auto'

    @staticmethod
    def get_benchmark() -> pd.Series:
        """設定對標報酬率的時間序列
        Returns:
          (pd.Series): 時間序列
        Examples:
            | date       |   0050 |
            |:-----------|-------:|
            | 2007-04-23 |   100 |
            | 2007-04-24 |   100.1 |
            | 2007-04-25 |   99 |
            | 2007-04-26 |   98.3 |
            | 2007-04-27 |   99.55 |
        """
        return pd.Series([], index=pd.Index([], dtype='datetime64[ns]'), dtype='float64')

    @staticmethod
    def get_asset_id_to_name() -> Dict:
        """設定對標報酬率的時間序列
        Returns:
          (dict): 股號與股名對照表，ex:`{'2330':'台積電'}`
        """
        return {}

    @staticmethod
    def get_price(trade_at_price:str, adj:bool=True) -> pd.DataFrame:
        """取得回測用價格數據
        Args:
           trade_at_price (str): 選擇回測之還原股價以收盤價或開盤價計算，預設為'close'。可選'close'或'open'。
           adj (str): 是否使用還原股價計算。
        Returns:
          (pd.DataFrame): 價格數據
        Examples:
            格式範例

            | date       |   0015 |   0050 |   0051 |   0052 |
            |:-----------|-------:|-------:|-------:|-------:|
            | 2007-04-23 |   9.54 |  57.85 |  32.83 |  38.4  |
            | 2007-04-24 |   9.54 |  58.1  |  32.99 |  38.65 |
            | 2007-04-25 |   9.52 |  57.6  |  32.8  |  38.59 |
            | 2007-04-26 |   9.59 |  57.7  |  32.8  |  38.6  |
            | 2007-04-27 |   9.55 |  57.5  |  32.72 |  38.4  |
            """
        return pd.DataFrame()

    @staticmethod
    def get_market_value():
        """取得回測用市值數據

        Returns:
          (pd.DataFrame): 市值數據

        """
        return pd.DataFrame()

    def get_trading_price(self, name: str, adj=True) -> pd.DataFrame:

        """取得回測用價格數據
        
        Args:
            name (str): 選擇回測之還原股價以收盤價或開盤價計算，預設為'close'。可選 'open'、'close'、'high'、'low'、'open_close_avg'、'high_low_avg'、或 'price_avg'。
        Returns:
            (pd.DataFrame): 價格數據

        """


        if name in ['open', 'close', 'high', 'low']:
            return self.get_price(name, adj=adj)
        elif name == 'close_open_avg' or 'open_close_avg':
            return (self.get_price('open', adj=adj) + self.get_price('close', adj=adj)) / 2
        elif name == 'high_low_avg' or 'low_high_avg':
            return (self.get_price('high', adj=adj) + self.get_price('low', adj=adj)) / 2
        elif name == 'price_avg':
            return (self.get_price('open', adj=adj) + self.get_price('close', adj=adj)\
                     + self.get_price('high', adj=adj) + self.get_price('low', adj=adj)) / 4

        raise ValueError(f"Unknown trade price name: {name}")



class TWMarketInfo(MarketInfo):

    @staticmethod
    def get_freq():
        return '1d'

    @staticmethod
    def get_name():
        return 'tw_stock'

    @staticmethod
    def get_benchmark() -> pd.Series:
        return finlab.data.get('benchmark_return:發行量加權股價報酬指數').squeeze()

    @staticmethod
    def get_asset_id_to_name():
        categories = finlab.data.get('security_categories')
        stock_names = dict(
            zip(categories.reset_index()['stock_id'], categories['name']))

        return stock_names

    @staticmethod
    def get_price(trade_at_price, adj=True):
        if isinstance(trade_at_price, pd.Series):
            return trade_at_price.to_frame()

        if isinstance(trade_at_price, pd.DataFrame):
            return trade_at_price

        if isinstance(trade_at_price, str):
            if trade_at_price == 'volume':
                return finlab.data.get('price:成交股數')

            if adj:
                table_name = 'etl:adj_'
                price_name = trade_at_price
            else:
                table_name = 'price:'
                price_name = {'open': '開盤價', 'close': '收盤價', 'high': '最高價', 'low': '最低價'}[trade_at_price]

            price = finlab.data.get(f'{table_name}{price_name}')
            return price

        raise Exception(f'**ERROR: trade_at_price is not allowed (accepted types: pd.DataFrame, pd.Series, str).')

    @staticmethod
    def get_market_value():
        return finlab.data.get('etl:market_value')


class USMarketInfo(MarketInfo):

    @staticmethod
    def get_freq():
        return '1d'

    @staticmethod
    def get_name():
        return 'us_stock'

    @staticmethod
    def get_benchmark():
        return finlab.data.get('world_index:adj_close')['^GSPC']

    @staticmethod
    def get_asset_id_to_name():
        categories = finlab.data.get('us_tickers')
        stock_names = dict(
            zip(categories['stock_id'], categories['name']))
        return stock_names

    @staticmethod
    def get_price(trade_at_price, adj=True):
        if isinstance(trade_at_price, pd.Series):
            return trade_at_price.to_frame()

        if isinstance(trade_at_price, pd.DataFrame):
            return trade_at_price

        if isinstance(trade_at_price, str):
            if trade_at_price == 'volume':
                return finlab.data.get('us_price:volume')

            if adj:
                table_name = 'us_price:adj_'
                price_name = trade_at_price
            else:
                table_name = 'us_price:'
                price_name = trade_at_price

            price = finlab.data.get(f'{table_name}{price_name}')
            return price

        raise Exception(f'**ERROR: trade_at_price is not allowed (accepted types: pd.DataFrame, pd.Series, str).')


class USAllMarketInfo(USMarketInfo):
    @staticmethod
    def get_price(trade_at_price, adj=True):
        if isinstance(trade_at_price, pd.Series):
            return trade_at_price.to_frame()

        if isinstance(trade_at_price, pd.DataFrame):
            return trade_at_price

        if isinstance(trade_at_price, str):
            if trade_at_price == 'volume':
                return finlab.data.get('us_price_all:volume')

            if adj:
                table_name = 'us_price_all:adj_'
                price_name = trade_at_price
            else:
                table_name = 'us_price_all:'
                price_name = trade_at_price

            price = finlab.data.get(f'{table_name}{price_name}')
            return price

        raise Exception(f'**ERROR: trade_at_price is not allowed (accepted types: pd.DataFrame, pd.Series, str).')

    @staticmethod
    def get_market_value():
        return finlab.data.get('us_fundamental:marketcap')


def get_market_info(df:Union[None, pd.DataFrame, pd.Series]=None, 
                    user_market_info:Union[None, str, MarketInfo]='AUTO') -> Optional[MarketInfo]:

    
    # return market info base on user_market_info
    if user_market_info == 'TW_STOCK':
        return TWMarketInfo()

    if user_market_info == 'US_STOCK':
        return USMarketInfo()

    if user_market_info == 'US_STOCK_ALL':
        return USAllMarketInfo()

    if user_market_info != 'AUTO':
        return user_market_info

    # deal with user_market_info == 'AUTO'
    if df is not None:
        ids = set([df.name]) if isinstance(df, pd.Series) else set(df.columns)
        for market in [TWMarketInfo(), USMarketInfo()]:
            market_ids = set(market.get_asset_id_to_name().keys())
            id_not_found = ids - market_ids

            if len(id_not_found) / len(ids) < 0.5:
                if len(id_not_found):
                    logging.warning(f"Symbols {str(id_not_found)[:30]}... not found in MarketInfo.")
                return market

    raise Exception("Market cannot be determined automatically. "
                    "Please set the market argument to either "
                    "'TW_STOCK' for Taiwan stock market, 'US_STOCK' "
                    "for US stock market, or use subclass of MarketInfo"
                    " to specify a different market.")


