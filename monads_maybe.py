
#Error Monads ---------------------
#----------------------------------

class Maybe:
	def __repr__(self):
		return str(self)
class Just(Maybe):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return str(self.value)
class Nothing(Maybe):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return self.msg
	
def unit(value):
	return Just(value)

def bind(mvalue, mfunc):
	if isinstance(mvalue, Nothing):
		return mvalue
	return mfunc(mvalue.value)


#------------------
if __name__=="__main__":
	def get_account(name):
		#f: a -> m b
	    if name == "Irek": return Just(1)
	    elif name == "John": return Just(2)
	    elif name == "Alex": return Just(3)
	    elif name == "Nick": return Just(1)
	    else: return Nothing("Account for {} not found".format(name))

	def get_balance(account):
		#f: a -> m b
	    if account == 1: return Just(1000000)
	    elif account == 2: return Just(75000)
	    else: return Nothing("Balance for {} not found".format(account))

	def qualified_amount(balance):
		#f: a -> m b
	    if balance > 200000: return Just(balance)
	    else: return Nothing("Balance {} insufficient".format(balance)) 
	 
	#function composint other functions
	def get_loan(name):
		#f: a -> m b
	    m_name =    unit(name)
	    m_account = bind(m_name, get_account)
	    m_balance = bind(m_account, get_balance)
	    m_loan =    bind(m_balance, qualified_amount)
	    return m_loan


	names = ["Irek", "John", "Alex", "Nick", "Fake"]
	
	for name in names:
		loan=get_loan(name)
		print "%s: %s" % (name, loan)
 