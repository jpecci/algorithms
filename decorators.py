import time

def time_func(f):
	"""time the running time of a function"""
	def helper(*args, **kargs):
		start=time.time()
		ans=f(*args, **kargs)
		end=time.time()
		dt=end-start
		if dt<60:
			msg="{0} took {1:.3f} secs".format(f.__name__, dt)
		else:
			msg="{0} took {1:.3f} mins".format(f.__name__, dt/60.)
		print msg
		return ans
	return helper

def mark_call(f):
	"""print an output any time the function is called"""
	def helper(*args, **kargs):
		ans=f(*args, **kargs)
		print "called {}".format(f.__name__)
		return ans
	return helper

@mark_call
def dummy1(x,y):
	return x+y

def dummy2(x,y):
	return x+y


if __name__=='__main__':
	
 	print dummy1(1, y=2)
 	print time_func(dummy2)(1,y=2)