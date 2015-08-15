import math
import numpy as np

class Sharpe:
	DAYS_IN_YEAR=252
	def __init__(self):
		self.cret=0
		self.cret2=0
		self.count=0
	def update(self, ret):
		self.cret+=ret
		self.cret2+=ret*ret
		self.count+=1
	def get_ret(self):
		"""return yearly return"""
		avg_daily_ret=self.cret/float(self.count)
		return avg_daily_ret*Sharpe.DAYS_IN_YEAR
	def get_vol(self):
		"""return yearly volatility"""
		count=float(self.count)
		var=(self.cret2-self.cret*self.cret/count)/count
		yearly_var=var*Sharpe.DAYS_IN_YEAR
		return math.sqrt(yearly_var)
	def get(self):
		"""return Sharpe Ratio"""
		return self.get_ret()/self.get_vol()
	def __repr__(self):
		return "sharpe={}, vol={}, ret={}".format(self.get(), self.get_vol(), self.get_ret())

class DrawDown:
	def __init__(self):
		self._resetTo(0)
		self.deepest_dd=(0,0) #(depth, duration)
	def _resetTo(self, value):
		self.max_value=value
		self.min_value=value
		self.duration=0
		self.in_dd=False
	def _current_dd(self):
		depth= self.max_value-self.min_value
		return (depth, self.duration)
	def update(self,value):
		if value>=self.max_value:
			if self.in_dd: #just exited from a dd
				self.deepest_dd=self.get_deepest() 
			self._resetTo(value)
		else:
			self.in_dd=True
			self.duration+=1  
			if value<self.min_value:
				self.min_value=value
	def get_deepest(self):
		current_dd= self._current_dd() 
		return current_dd if current_dd[0]>self.deepest_dd[0] else self.deepest_dd
	def __repr__(self):
		depth, duration=self.get_deepest()
		return "depth={}, duration={}".format(depth, duration)
		
class VAR:
	def __init__(self):
		self.values=[]
	def update(self, value):
		self.values.append(value)
	def _get_index_thr(self, threshold):
		return int((1-threshold)*len(self.values))
	def get(self, threshold=0.95):
		index=self._get_index_thr(threshold)
		return sorted(self.values)[index]
	def get_es(self, threshold=0.95):
		index=self._get_index_thr(threshold)
		return np.mean(sorted(self.values)[:index])
	def __repr__(self):
		return "{}".format(self.get())


if __name__=="__main__":
	from data import load_data
	file="/Users/jacopo/Downloads/table.csv"
	data=load_data(file)
	sharpe=Sharpe()
	dd=DrawDown()
	for i in xrange(len(data)):
		if i>0:
			ret=data[i][4]/data[i-1][4]-1
			sharpe.update(ret)
		dd.update(data[i][4])
	print sharpe
	print dd

