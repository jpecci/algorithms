from fractions import Fraction


class Price32:
	def __init__(self, value, *args):
		"""
		accepted constructors:
		Price32(10), Price32(10,1,32), Price32(10, Fraction(1,32))
		"""
		self.value=value

		if len(args)==0:
			self.frac=Fraction(0)
		elif len(args)==1 and isinstance(args[0], Fraction):
			frac=args[0]
			self.frac=frac
		elif len(args)==2 and isinstance(args[0], int) and isinstance(args[1], int):
			num, den=args
			self.frac=Fraction(num, den)
 		else:
 			raise Exception("wrong arguments")

 		self._simplify()

 	def _simplify(self):
 		f=self.frac
 		if f.numerator>=f.denominator:
 			self.value+= int(f.numerator/f.denominator)
			self.frac= Fraction(f.numerator%f.denominator, f.denominator)
 	 


	def __add__(self, other):
		if isinstance(other, Price32):
			return Price32(self.value+other.value, self.frac+other.frac)
		elif isinstance(other, int):
			return Price32(self.value+other, self.frac)
		elif isinstance(other, Fraction):
			#TODO 5 1/32 - 1/16 does not work
			return Price32(self.value, self.frac+other)
		else:
			raise Exception("can only add int or Price32")
		 
	def __neg__(self):
		return Price32(-self.value, -self.frac)

	def __sub__(self, other):
		return self+(-other)


	def __mul__(self, other):
		if isinstance(other, Price32):
			return self.toFloat()*other.toFloat()
		elif isinstance(other, int):
			return Price32(self.value*other, self.frac*other)
		elif isinstance(other, float):
			return self.toFloat()*other

		"""
		if isinstance(other, Price32):
			value=self.value*other.value
			frac=self.value*other.frac + self.frac*other.value + self.frac*other.frac
			return Price32(value, frac)
		"""

	def __div__(self, other):
		if isinstance(other, Price32):
			return self.toFloat()/other.toFloat()
		return self.toFloat()*(1.0/other)

	def __str__(self):
		return "{:d} {:d}/{:d}".format(self.value, abs(self.frac.numerator), self.frac.denominator)
	def __repr__(self):
		return str(self)
	def toFloat(self):
		return self.value+float(self.frac.numerator)/self.frac.denominator



p1=Price32(5,1,32)
p2=Price32(5)
p3=Price32(5, Fraction(1,16))
print p1,p2,p3
print -p1
print p1+p1
print p1-p1