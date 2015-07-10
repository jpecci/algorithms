import itertools as it

def flatten(xss):
	"""flatten a list of a list"""
	return [x for xs in xss for x in xs]
def iflatten(xss):
	for xs in xss:
		for x in xs:
			yield x

def flatMap(xs, op):
	return flatten(map(op, xs))
def iflatMap(xs, op):
	return iflatten(it.imap(op,xs))

def foldRight(zero, op):
	"""op(x0, op(x1, op(x2,zero)))"""
	def helper(xs):
		y=zero
		for x in xs[::-1]:
			y=op(x,y)
		return y
	return helper

def foldRight_(xs, zero, op):
	"""op(x0, op(x1, op(x2,zero)))
	recursive implementation"""
	def helper(ys, acc):
		if len(ys)==0:
			return acc
		acc=op(ys[-1],acc)
		return helper(ys[:-1],acc)

	return helper(xs, zero)


def foldLeft_(xs, zero, op):
	"""op(op(op(zero,x0), x1), x2)
	recursive implementation"""
	def helper(ys, acc):
		if len(ys)==0:
			return acc
		acc=op(acc,ys[0])
		return helper(ys[1:],acc)
	
	return helper(xs, zero)

def foldLeft(zero, op):
	"""op(op(op(zero,x0), x1), x2)"""
	def helper(xs):
		y=zero
		for x in xs:
			y=op(y,x)
		return y
	return helper


if __name__=="__main__":
	import operator
	xs=[1.,2.,3.]
	print foldRight(1, operator.div)(xs)
	print foldRight_(xs, 1, operator.div) 
	print foldLeft(1, operator.div)(xs)
	print foldLeft_(xs, 1, operator.div)
	print flatten([[1,2,3],[4,5]])