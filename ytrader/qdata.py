import numpy as np
import pandas as pd
import datetime as dt
import jpholiday as jh
import investpy
import time


class Symbol:
    def __init__(self, code, tradetime, duration):
        """
        Parameters
        ----------
        code : int
            銘柄コード/商品ID
        attr : dict
            銘柄の財務情報
        duration : int
            価格データの日数
        price : DataFrame
            価格データ
        time  : Tradetime
            日時
        """
        start = time.time()
        self.code = code
        self.duration = duration
        self.time = tradetime
        self.get_attr()
        self.get_data()
        print("Loaded %d" % code, time.time()-start)
    
    def preprocess(self):
        pass

    def update(self):
        """
        Symbolクラスの価格データを本日に更新する.
        self.priceの最後の行が本日でなければ、休日チェックの後に価格データを追加する.
        """
        if (self.time.time != self.price.index[-1].date()):
            self.get_data()
        self.preprocess()

    # Utils function
    def get_attr(self):
        self.attr = {}

    def get_data(self):
        begin = self.time.previous_date(self.duration)
        self.price = self.get_single_series(self.code, begin, self.time.time)
        self.spot = self.price.Close[-1]

    def get_single_series(self, code, begin_date, end_date, country_name='japan'):
        '''
        Download single data by using investpy.
        Parameters
        ----------
        code: str
            four-digit code of which you want historical data
        begin_date: str or datetime.date
            Begin date ex.15/6/2020
        end_date: str or datetime.date
            End dates
        Returns
        -------
        price_data['Close']: pd.Series
        '''
        code = str(code)
        if isinstance(begin_date, dt.date):
            begin_date = begin_date.strftime("%d/%m/%Y")
        if isinstance(end_date, dt.date):
            end_date = end_date.strftime("%d/%m/%Y")

        price_data = investpy.get_stock_historical_data(
            stock=code,
            country=country_name,
            from_date=begin_date,
            to_date=end_date
        )
        # DataFrameに変更
        price_series = price_data[['Close']]
        price_series.name = code
        return price_series


class Qdata:
    """
    銘柄情報・価格データ・経済データ・時間を一元管理するオブジェクト
    一つのトレーディングシステムにつき一つ
    このクラスの行動範囲はデータ収集からデータ前処理まで
    継承先で特徴量テーブルを作成する。  
    """

    def __init__(self, tradetime, symbol, duration=100):
        """
        Parameters
        ----------
        symbol : Object like Symbol
                任意の銘柄クラス
        data : dict
                分析用補助データ
        time : Tradetime
                現在の日
        """
        self.symbol_gen = symbol
        self.symbols = []
        self.data = {}
        self.time = tradetime
        self.duration = duration

    def update(self):
        """
        各symbolクラスのupdateメソッドを呼び出す。
        """
        for s in self.symbols:
            s.update()

    def set_duration(self, day_n):
        self.duration = day_n

    # interface
    def all_price(self):
        """
        symbolの価格データを合体して返す。
        """
        return pd.concat([t.price.add_prefix(str(t.code)+'_') for t in self.symbols], axis=1)

    def get_codes(self):
        return [t.code for t in self.symbols]

    def add_symbols(self, code):
        """
        Qdataに新たな銘柄を追加する

        Parameters
        ----------
        code : int or list<int>
        """
        if isinstance(code, int):
            sym = self.symbol_gen(code, self.time, self.duration)
            sym.update()
            self.symbols.append(sym)
        elif isinstance(code, list):
            # 時間がかかるかも
            for c in code:
                sym = self.symbol_gen(c, self.time, self.duration)
                sym.update()
                self.symbols.append(sym)

    def get_symbol(self, code):
        """
        指定した銘柄オブジェクトを渡す。コピーではなく参照になっててほしい。
        """
        for s in self.symbols:
            if s.code == code:
                return s
        return 0
