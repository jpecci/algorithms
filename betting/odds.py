import numpy as np
from fractions import gcd
import itertools as it

class OddsDec:
	EPSILON=0.0000001
	def __init__(self, value):
		if value<1:
			raise Exception("Invalid value for decimal odds: ",value)
		self.value=float(value)
	def pnl_back(self, event_occured, capital):
		if event_occured:
			return capital*(self.value-1)
		return -capital
	def pnl_lay(self, event_occured, capital):
		return -self.pnl_back(event_occured, capital)
	def toProb(self):
		return 1.0/self.value
	def __add__(self, that):
		prob=self.toProb()+that.toProb()
		return OddsDec(1.0/prob)
	def __eq__(self, that):
		delta=self.value-that.value
		return delta < OddsDec.EPSILON and delta > -OddsDec.EPSILON 
	def __repr__(self):
		return "{0}".format(self.value)
	def __str__(self):
		return self.__repr__()

class OddsFrac:
	"""
	Fractional odds expressed as 3/2 where a=3 and b=2
	Implied probability is b/(b+a)
	"""
	def __init__(self, a,b):
		div=gcd(a,b)
		self.a=a/div
		self.b=b/div
 
	def pnl_back(self, event_occured, capital):
		if event_occured:
			return self.__normalize()*capital
		return -capital
	def pnl_lay(self, event_occured, capital):
		return -self.pnl_back(event_occured, capital)
	def toProb(self):
		return float(self.b)/(self.b+self.a)
	def toDec(self):
		"""Decimal format, i.e. total winning amount"""
		return OddsDec(1+self.__normalize())
	def __normalize(self):
		"""return x where it is x/1"""
		return float(self.a)/self.b

	def __add__(self, that):
		"""
		to derive this formula: 
		1)convert the odds into probs
		2)sum the two probs
		3)convert the sum back to odds. 
		This way the implied probability is preserved.
		"""
		num=self.a*that.a-self.b*that.b
		den=2*self.b*that.b+self.b*that.a+that.b*self.a
		return Odds(num, den)

	def __eq__(self, that):
		return self.a==that.a and self.b==that.b
	def __repr__(self):
		return "{0}/{1}".format(self.a, self.b)
	def __str__(self):
		return self.__repr__()

def Odds(value1,value2=None):
	if value2 is None:
		return OddsDec(value1)
	else:
		return OddsFrac(value1,value2)

def compute_pnl(os,caps,wins):
	pnls=[(o.pnl(cap) if win else -cap) for o,cap,win in zip(os,caps,wins)]
	return sum(pnls)

def isArgitrage(os):
	prob=sum([o.toProb() for o in os])
	return True if prob <1 else False 

def capitalAllocation(o1,o2, capital=100):
	if not isArgitrage([o1,o2]):
		raise Exception("capitalAllocation without arbitrage opportunity")

	cap1_min= capital*o1.toProb()
	cap1_max= capital*(1-o2.toProb())
	#maximize the most probable outcome
	cap1= cap1_max if o1.toProb()>o2.toProb() else cap1_min

	return (cap1, capital-cap1)

def combination(num_outcomes, num_brokers):
	broker_index=range(num_brokers)
	return it.product(broker_index, repeat=num_outcomes)

def strat_back_lay(o_up, o_dw, cap_up, fee):
	"""
	cap_up/(1-fee) < cap_dw < cap_up*(o_up-1)/(o_dw-1)
	the value that make equal profit for any outcome is:
	cap_dw=cu*o_up/(o_dw-fee)
	"""
	cap_dw=cu*o_up/(o_dw-fee)
	stake_dw=cap_dw*(o_dw-1)
	profit=-cap_up+cap_dw*(1-fee)
	return stake_dw, profit


def allocate_capital(o1,o2,o3, cap=100):
	"""footbal 1x2"""
	min1=cap/(1+o1.normalize())
	min2=cap/(1+o2.normalize())
	A=(min1, min2)
	q=cap*o3.normalize()/(1+o3.normalize())
	B=(min1, -min1+q)
	C=(-min2+q, min2)
	if B[1]<=A[1] or C[0]<=A[0]:
		return (0,0,0)

	cap1=(A[0]+B[0]+C[0])/3.0
	cap2=(A[1]+B[1]+C[1])/3.0
	return (cap1, cap2, cap-cap1-cap2)

if __name__=="__main__":
	os=[]
	os.append([Odds(1.16), Odds(5.5), Odds(15.0)])
	os.append([Odds(1.2), Odds(5.25), Odds(13.25)])

	for idxs in combination(3,2):
		check_os=[]
		for j,idx in enumerate(idxs):
			check_os.append(os[idx][j])
		probs=sum([o.toProb() for o in check_os])
		print "%s (%.3f) %s"%(isArgitrage(check_os), probs, check_os)
