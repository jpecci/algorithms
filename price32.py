from fractions import Fraction


def toFraction(value, num, den):
	return Fraction(value*den+num, den)



class Price32(Fraction):
	#TODO make it work as a sub class of Fraction and inherit all for free
	def __new__(cls, *args):
			 
		"""
		accepted constructors:
		Price32(10), Price32(10,1,32)
		"""
		self=Fraction.__new__(cls)

		if len(args)==1:
			self._numerator=args[0]
			self._denominator=1
		elif len(args)==3:
			value, num, den=args
			frac=toFraction(value, num, den)
			self._numerator=frac.numerator
			self._denominator=frac.denominator
 		else:
 			raise Exception("wrong arguments")

 		return self
 	
 	def to32(self):
		value=self.numerator//self.denominator
	 	num=self.numerator%self.denominator
		den=self.denominator
		return (value, num, den)

	def toFloat(self):
		return float(self.numerator)/self.denominator


	def __str__(self):
		value, num, den = self.to32()
		return "{:d} {:d}/{:d}".format(value, num, den)
	def __repr__(self):
		return str(self)
	



p1=Price32(5,1,32)
p2=Price32(5)

print p1
print p2
print -p1
print p1+p1
print p1-p1
print p1*p1
print p1/p1
