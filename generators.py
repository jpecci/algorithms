import itertools as it
from timeutils import get_date, get_time, get_month, get_day, get_hour

def file_reader(filename, separator=','):
	with open(filename) as fp:
		for line in fp:
			timestamp, value=[tk.strip() for tk in line.split(separator)]
			yield (int(timestamp), float(value))


def max_per_period(iter, period):
	for period, i in it.groupby(iter, period):
		yield max(i, key=lambda (ts,v):v)

if __name__=='__main__':
	fn='/Users/jacopo/Downloads/dummy.csv'
	i=max_per_period(file_reader(fn), lambda (ts,v): get_day(get_date(ts)))
	