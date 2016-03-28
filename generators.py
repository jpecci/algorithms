import itertools as it
from timeutils import get_date, get_time, get_month, get_day, get_hour
import operator
from fractions import Fraction

def file_reader(filename, separator=','):
	with open(filename) as fp:
		for line in fp:
			timestamp, value=[tk.strip() for tk in line.split(separator)]
			yield (int(timestamp), float(value))


def max_per_period(iter, period):
	for period, i in it.groupby(iter, period):
		yield max(i, key=lambda (ts,v):v)

def factorial(n):
	return reduce( operator.mul, range(1, n+1), 1)

def sum_series( terms, epsilon=1E-8 ):
	iterator=it.takewhile(lambda x:abs(x)>epsilon, terms)
	return sum(iterator)

def partial_gamma_series(s,z,epsilon=1E-8):
	def terms(s,z):
		for k in xrange(100):
			t1=Fraction(z**(s+k), s+k)
			t2=Fraction( (-1)**k, factorial(k))
			yield t1*t2
	return float(sum_series( terms(s,z), epsilon ))
 
if __name__=='__main__':
	fn='/Users/jacopo/Downloads/dummy.csv'
	i=max_per_period(file_reader(fn), lambda (ts,v): get_day(get_date(ts)))
	