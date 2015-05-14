import itertools as it

def file_reader(filename, separator=','):
	with open(filename) as fp:
		for line in fp:
			tks=[tk.strip() for tk in line.split(separator)]
			yield (int(tks[0]), float(tks[1]))

get_time=lambda date: date%10000
get_min =lambda date: get_time(date)%100
get_hour =lambda date: get_time(date)//100

get_date=lambda date: date//10000
get_day=lambda date: get_date(date)%100
get_month=lambda date: (get_date(date)%10000)//100
get_year=lambda date: get_date(date)//10000





if __name__=='__main__':
	fn='/Users/jacopo/Downloads/dummy.csv'
	reader=file_reader(fn)
	for hour, iterator in it.groupby(reader, lambda item:get_year(item[0])):
		print "hour={}, len={}".format(hour, len(list(iterator)))
