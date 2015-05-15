import itertools as it
from timeutils import get_date, get_time, get_month, get_day, get_hour

def file_reader(filename, separator=','):
	with open(filename) as fp:
		for line in fp:
			timestamp, value=[tk.strip() for tk in line.split(separator)]
			yield (int(timestamp), float(value))





if __name__=='__main__':
	fn='/Users/jacopo/Downloads/dummy.csv'
	reader=file_reader(fn)
	for hour, iterator in it.groupby(reader, lambda item:get_hour(get_time(item[0]))):
		print "hour={}, len={}".format(hour, len(list(iterator)))
