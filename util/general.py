import time

def time_func(f,*args):
	print "%s running..."%f.__name__
	start=time.time()
	res=f(*args)
	end=time.time()
	print "\tfinished in %.4f mins"%( (end-start)/60.)
	return res