import datetime as dt
#import ytrader as yt
import ytrader as yt

class MAsymbol(yt.Symbol):
	def __init__(self, code, tradetime, duration):
		super().__init__(code, tradetime, duration)
		self.sma = 6
		self.lma = 12
	def preprocess(self):
		self.price['sma']=self.price['Close'].rolling(self.sma).mean()
		self.price['lma']=self.price['Close'].rolling(self.lma).mean()

class MAstrategy(yt.Strategy):
	def trade(self):
		for c in self.universe:
			sym = self.qdata.get_symbol(c)
			buy_condition = sym.price['sma'][-1] > sym.price['lma'][-1]
			pos_id = self.book.get_id_bycode(c)
			if pos_id:
				#exit
				if not buy_condition:
					self.book.exit(pos_id)
				
			else:
				#entry
				if buy_condition:
					order = (c,1,10)
					self.book.entry(*order)

universe = [3807,4502,1352]
# #live trade
# trader = Trader(MAsymbol,Qdata, MAstrategy,universe)
# trader.live()
# trader.run()

#backtest
trader = yt.Trader(MAsymbol,yt.Qdata, MAstrategy,universe)
begin = dt.date(2021,8,1)
end = dt.date(2021,8,8)
trader.bt(begin,end)
trader.run()