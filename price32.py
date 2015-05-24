from fractions import Fraction


class Price32(Fraction):
	def __new__(cls, *args):
		return Fraction.__new__(cls, args)
	def __init__(self, *args):
		"""
		accepted constructors:
		Price32(10), Price32(10,1,32)
		"""
		
		if len(args)==1:
			Fraction.__new__(args[0])
		elif len(args)==3:
			value, num, den=args
			Fraction.__new__(value*den+num, den)
 		else:
 			raise Exception("wrong arguments")

 	def _express_in_32(self):
 		value=self.numerator//self.denominator
 		num=self.numerator%self.denominator
		den=self.denominator
		return value, num, den
		


	def __str__(self):
		value, num, den = self._express_in_32()
		return "{:d} {:d}/{:d}".format(value, num, den)
	def __repr__(self):
		return str(self)
	def toFloat(self):
		return float(self.numerator)/self.denominator



p1=Price32(5,1,32)
p2=Price32(5)
p3=Price32(5, Fraction(1,16))
print p1,p2,p3
print -p1
print p1+p1
print p1-p1