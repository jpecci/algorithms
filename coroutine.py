from functools import partial




def producer(text,next_step):
	for word in text.split(" "):
		next_step.send(word)
	next_step.close()

def filter1(next_step):
	try:
		while True:		
			word=(yield)
			word_lower=word.lower()
			next_step.send(word_lower) 
	except GeneratorExit as e:
		next_step.close()	

def filter2(next_step): 
	try:
		while True:
			word=(yield)
			if "a" in word:
				next_step.send(word)
	except GeneratorExit as e:
		next_step.close()

def consumer(): 
	try:
		while True:
			word=(yield)
			print word
	except GeneratorExit as e:
		print "All closed"



if __name__=="__main__":

	text="""Mi chiamo JAcopo e sto facendo un test per 
	testare come funzionAno le coroutine."""

	#you have to create from the last (consumer) to the first (producer)
	c=consumer()
	c.next()
	
	f2=filter2(c)
 	f2.next()

	f1=filter1(f2)
	f1.next()

	producer(text,f1)
