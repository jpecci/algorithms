import heapq as hq
import datetime as dt
import time



class Event:
	def __init__(self, start, func, args, period=None, end=None):
		self.start=start
		self.func=func
		self.args=args
		self.period=period
		self.end=end

	def is_recurring(self):
		return self.end is not None
	
	def shoot(self):
		self.func(self.args)

	def get_next(self):
		next_start=self.start+self.period
		if next_start<self.end:
			return Event(next_start, self.func, self.args, self.period, self.end)
		return None
		
	def __le__(self, that):
		return self.start<= that.start
	def __eq__(self, that):
		return self.start == that.start


class Scheduler:
	def __init__(self, frequency=1, shutdown=None):
		"""
		frequency: how many time per second it checks for events
		shutdown: when to stop the scheduler even if there are still
		events in the queue	
		"""
		self.events=[]
		self.frequency=frequency
		self.shutdown=shutdown

	def register(self, event):
		hq.heappush(self.events, event)
	
	def __keep_running(self):
		if len(self.events)==0:
			return False

		return True if (self.shutdown is None) else self.shutdown>dt.datetime.now()
		 
	def run(self):
		while self.__keep_running():
			event=self.events[0]
			now=dt.datetime.now()
			print "checking %s..."%(now)
			if now>=event.start:
				event.shoot()
				hq.heappop(self.events) 
				#create a new one of it was recurring
				if event.is_recurring():
					new_event=event.get_next()
					if new_event:
						self.register(new_event)
			else:
				time.sleep(1./self.frequency)



if __name__=="__main__":
	def test(arg):
		print "test %s"%arg
		
	now=dt.datetime.now()
	sc=Scheduler(1)
	e1=Event(now+dt.timedelta(seconds=3), test, "start in 3", dt.timedelta(seconds=10), now+dt.timedelta(seconds=30))
	e2=Event(now+dt.timedelta(seconds=5), test, "start in 5")
	e3=Event(now+dt.timedelta(seconds=10), test, "start in 10")
	sc.register(e2)
	sc.register(e1)
	sc.register(e3)
	sc.run()
