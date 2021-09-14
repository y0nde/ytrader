import numpy as np
import pandas as pd
import datetime as dt
import tradetime

class Position:
	def __init__(self,id,entry_t,symbol,direction,quantity):
		"""
		Parameters
		----------
		id : int
		entry_t : Datetime.Date
		symbol : Symbol
		direction  : int
			long: 1
			short : -1
		quantity : int
		entry_flag : bool
		spot : int
		"""
		self.id = id
		self.entry_t=entry_t
		self.exit_t=None
		self.symbol=symbol
		self.direction=direction
		self.quantity=quantity
		self.entry_flag=True
	
	def detail(self):
		out=self.__dict__.copy()
		out['symbol']=self.symbol.code
		out['spot']=self.spot()
		return out

	def spot(self):
		#このままだとイグジット済みでもspotが変化してしまう
		#今のところ他に影響なし
		return self.quantity * self.symbol.spot
	
	def __str__(self):
		return self.code

class Book:
	def __init__(self,qdata,tradetime):
		"""
		Parameters
		----------
		qdata : Qdata
		time : Tradetime
		positions : list<Position>
		initial_balance : int
		book_detail : DataFrame
						index : pd.Timestamp
						row : ['position_num','entry_num','exit_num','balance'] 
		"""
		self.qdata=qdata
		self.time=tradetime
		self.positions=[]
		self.initial_balance=1000000
		self.cash=self.initial_balance
		self.detail=pd.DataFrame(columns=['positions','in_entry','cash','balance'])
		self.order_count=0

	def update(self,p=True):
		"""
		ポジション数・残高を再計算してbook_detailに追加
		"""
		l=len(self.positions)
		en=sum([p.entry_flag for p in self.positions])
		#???balanceは現金とポジションのスポット価格を足す
		self.balance=self.cash + sum([int(p.entry_flag)*int(p.spot()) for p in self.positions])
		row=[l,en,self.cash,self.balance]
		self.detail.loc[self.time.time]=row
		self.show_positions()
		if p:
			print(self.detail)

	def entry(self,code,direction,quantity):
		symbol=self.qdata.get_symbol(code)
		if symbol:
			if self.cash < (symbol.spot*quantity):
				print("Can't entry (lack of money)")
				return -1
			else:
				self.order_count+=1
				self.cash -= (symbol.spot*quantity)
				pos=Position(self.order_count,self.time.time, symbol, direction, quantity)
				self.positions.append(pos)
				return id

	def exit(self,id):
		"""
		positionのエントリーフラグとイグジット時間を設定し、現金残高に戻す。
		"""
		pos = self.get_pos(id)
		pos.entry_flag=False
		pos.exit_t=self.time.time
		self.cash += pos.spot()
		return id

	def get_pos(self,id):
		for p in self.positions:
			if p.id == id:
				return p
		return 0
	
	def get_id_bycode(self,code):
		for p in self.positions:
			if p.symbol.code == code:
				if p.entry_flag:
					return p.id
		return 0

	def show_positions(self):
		print('\n',self.time.time)
		for p in self.positions:
			print(p.detail())