from heap import HeapMax
from heapq import heappush, heappop

class Median:
	def __init__(self):
		#unfortunatelly min and max have different interfaces
		self.max=HeapMax()
		self.min=[]
	
	def get(self):
		diff=len(self.max.v)-len(self.min)
		if diff>0: #it should not be >1
			key,obj=self.max.top()
			return key
		elif diff<0:
			return self.min[0]
		else:
			key,obj=self.max.top()
			return (key+self.min[0])/2.0
		
	def add(self, value):
		sz=self.size()
		if sz == 0:
			#push it anywhere
			self.max.push(value)

		elif sz==1:
			if len(self.min)>0:
				right=self.min[0]
				if value>right:
					heappush(self.min,value)
				else:
					self.max.push(value,None)
			else:
				left, obj=self.max.top()
				if value<left:
					self.max.push(value,None)
				else:
					heappush(self.min,value)
		
		else: 
			#for sure three are items in both the heaps
			right=self.min[0]
			if value>right:
				heappush(self.min,value)
			else:
				self.max.push(value,None)
			
		self.__rebalance()
	
	def size(self):
		return self.max.size+len(self.min)

	def __rebalance(self):
		diff=self.max.size-len(self.min)
		if diff>1:
			value,obj=self.max.pop()
			heappush(self.min,value)
		elif gap<-1:
			value=heappop(self.min)
			self.max.push(value,None)
		else:
			pass


if __name__=="__main__":
	m=Median()
	for i in xrange(10):
		m.add(i)
		print m.get()
