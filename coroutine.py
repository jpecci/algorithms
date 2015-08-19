from functools import partial

#this decorator makes the call to next() not needed
def coroutine(func):
	def helper(*args,**kwargs):
		f = func(*args,**kwargs)
		f.next()
		return f
	return helper

#the decorator is not needed because this is not a generator
#i.e. it does not have yield
def producer(file, next_step):
	with open(file) as fp:
		for line in fp:
			for word in line.split(" "):
				next_step.send(word)
	next_step.close()

@coroutine
def filter1(next_step):
	try:
		while True:		
			word=(yield)
			word_lower=word.lower()
			next_step.send(word_lower) 
	except GeneratorExit as e:
		next_step.close()	

@coroutine
def filter2(pattern, next_step): 
	try:
		while True:
			word=(yield)
			if pattern in word:
				next_step.send(word)
	except GeneratorExit as e:
		next_step.close()

@coroutine
def consumer(): 
	#the consumer does is the last step of the pipe
	try:
		while True:
			word=(yield)
			print word
	except GeneratorExit as e:
		print "All closed"

"""
This could be implemented with simple generators:
The difference is that generators pull data, while
coroutines push the data. Also with coroutines you can 
send the data to multiple steps in paraller (they provide more 
flexible routing options)

 
def producer(file):
	with open(file) as fp:
		for line in fp:
			for word in line.split(" "):
				print "producer"
				yield word

def filter1(iterator):
	for word in iterator:	
		print "filter1"		
		word_lower=word.lower()
		yield word_lower 	

def filter2(pattern, iterator): 
	for word in iterator:
		print "filter2"
		if pattern in word:
				yield word 

def consumer(iterator): 
	for word in iterator:
		print "consumer"
		print word
	

file="/Users/jacopo/Downloads/alice.txt"
consumer(filter2("dog",filter1(producer(file))))

"""

if __name__=="__main__":

	text="""Mi chiamo JAcopo e sto facendo un test per 
	testare come funzionAno le coroutine."""
	file="/Users/jacopo/Downloads/alice.txt"
	#you have to create from the last (consumer) to the first (producer)
	c=consumer()
	#c.next()
	
	f2=filter2("dog",c)
 	#f2.next()

	f1=filter1(f2)
	#f1.next()

	producer(file,f1)

	producer(file,filter1(filter2("ago", consumer())))
