def foldRight_(xs, zero, op):
	#op(x0, op(x1, op(x2,zero)))
	def helper(ys, acc):
		if len(ys)==0:
			return acc
		acc=op(ys[-1],acc)
		return helper(ys[:-1],acc)

	return helper(xs, zero)

def foldRight(xs, zero, op):
	#op(x0, op(x1, op(x2,zero)))
	y=zero
	for x in xs[::-1]:
		y=op(x,y)
	return y

def foldLeft_(xs, zero, op):
	#op(op(op(zero,x0), x1), x2)
	def helper(ys, acc):
		if len(ys)==0:
			return acc
		acc=op(acc,ys[0])
		return helper(ys[1:],acc)
	
	return helper(xs, zero)

def foldLeft(xs, zero, op):
	#op(op(op(zero,x0), x1), x2)
	y=zero
	for x in xs:
		y=op(y,x)
	return y

if __name__=="__main__":
	import operator
	xs=[1.,2.,3.]
	print foldRight(xs, 1, operator.div)
	print foldRight_(xs, 1, operator.div)
	print foldLeft(xs, 1, operator.div)
	print foldLeft_(xs, 1, operator.div)