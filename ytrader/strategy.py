class Strategy:
	"""
	アルゴトレードの戦略部分です。
	内部の流れ
	1. Qdataから金融データを取り込み、計算処理
	2. エントリー・イグジット条件
	3. Bookに対して発注
	ペアトレーディングのように複数の状態を管理しなければならない場合は、
	Qdataに標準化・検定などの前処理機能を追加
	Strategyではペアの管理機能を追加
	するなど適切な機能の配分を目指してください。
	"""
	def __init__(self,tradetime,qdata,book,universe):
		"""
		Parameters
		----------
		time : Tradetime
			取引時間管理
		qdata : Qdata
			金融データ群
		book : Book
			ポジション管理
		universe : list<int>
			対象とする銘柄群
		"""
		self.time=tradetime
		self.qdata=qdata
		self.book=book
		self.universe=universe
		self.add_symbols(self.universe)
	
	def trade(self):
		pass

	def __str__(self):
		return 'Strategy'
	
	def add_symbols(self,codes : list):
		syms=self.qdata.get_codes()
		for c in codes:
			if c not in syms:
				self.qdata.add_symbols(c)