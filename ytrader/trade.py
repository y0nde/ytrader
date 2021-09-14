import datetime as dt
from tradetime import Tradetime
from book import Book


class Trader:
	"""
	Traderはライブトレードとバックテストで動きが変化する。
	ライブトレード時はリアル時間との同期に加え、
	当プロセスが中断しても各クラスの状態が保存するように注意する。
	バックテスト時は開始・終了の期間に注意。
	"""
	def __init__(self,symbol,qdata ,strategy,universe,bt=False):
		"""
		カスタマイズしたSymbol・Qdata・Strategyクラスをセットする。
		もし、book・tradetimeを

		Parameters
		----------
		# must param
		qdata : Qdata_constructer
		strategy : Strategy_constructer

		# auto set param
		time : Tradetime
		book : Book
		"""
		self.bt_flag=bt
		self.time=Tradetime()
		self.qdata=qdata(self.time,symbol)
		self.book=Book(self.qdata, self.time)

		self.strategy=strategy(self.time,self.qdata,self.book,universe)

		self.begin=None
		self.end=None
	
	def live(self):
		self.bt_flag=False

	def bt(self,begin,end):
		self.bt_flag=True
		self.begin=begin
		self.end=end
	
	def run(self):
		if self.bt_flag:
			if not (bool(self.begin) & bool(self.end)):
				print("please set time.")
				return -1
			self.time.set_time(self.begin)
			self.qdata.update()
			while True:
				#当日の行動　取引＆資産確認
				self.strategy.trade()
				self.book.update()

				#翌日への更新 時間更新（break)＆データ更新
				if self.end == self.time.time:
					break
				self.time.update()
				self.qdata.update()
		else:
			# ライブトレード
			
			self.time.set_time()
			# 各オブジェクトのロード

			# 各オブジェクトの更新・トレード
			self.qdata.update()
			self.strategy.trade()
			self.book.update()

			# 各オブジェクトの保存
