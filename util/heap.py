
from math  import floor
import heapq

class HeapLookUp:
	"""
	Canonical heap with the addition of a dictionary
	storing the index positions of the objects in the heap.
	This allows a constant time lookup - faster than in 
	the standard heap implementation.
	"""

	iTOP=1 #index of the first element, ie the min element
	def __init__(self):
		self.v=[None] #(key,obj) exclude v[0] for semplicity
		self.idx={} #(obj:idx)
		self.size=0
	def __lastIndex(self):
		#last element is not (size-1) since we start from index 1
		return self.size  

	def __parent(self,i):
		return int(floor(i/2))

	def __childL(self,i):
		return int(2*i)
	
	def __childR(self,i):
		return int(2*i+1)
	
	def __bubbleUp(self,i):
		 
		while i>HeapPlus.iTOP:
			key=self.v[i][0]
			i_parent=self.__parent(i)
			key_parent=self.v[i_parent][0]

			if key < key_parent:
				self.__swap(i, i_parent)
				i=i_parent
			else:
				break 
		return i
			
	def __bubbleDwn(self,i):
		
		while i<self.__lastIndex():
			key=self.v[i][0]

			i_childL=self.__childL(i)
			i_childR=self.__childR(i)

			if i_childL <=self.__lastIndex():
				i_child=i_childL
				if i_childR<=self.__lastIndex():
					#if there are 2 children choose the one  with smallest key
					i_child= i_childL if self.v[i_childL][0]<self.v[i_childR][0] else i_childR
	
				key_child=self.v[i_child][0]
			
				if key_child < key:
					self.__swap(i, i_child)
					i=i_child
				else:
					break
			else:
				break
		return i

	def __swap(self,i,j):
		#first update idx
		obj_i=self.v[i][1]
		self.idx[obj_i]=j
		
		obj_j=self.v[j][1]
		self.idx[obj_j]=i

		#then swap
		temp=self.v[i]
		self.v[i]=self.v[j]
		self.v[j]=temp
	
	def push(self, key, obj):
		if obj not in self.idx:
			self.v.append((key,obj))
			self.size+=1

			i=self.__bubbleUp(self.__lastIndex())  
		
			self.idx[obj]=i
		else:
			print "%s already in heap. Not added!"%(obj)

	def pop(self):
		return self.__remove_idx(HeapPlus.iTOP)
		
	def lookup(self, obj):
		#return (key, obj)
		if obj in self.idx:
			return self.v[self.idx[obj]]
		return None 

	def __remove_idx(self, i):
		#move to the last position
		self.__swap(i, self.__lastIndex())

		rem_key, rem_obj=self.v.pop() 
		self.size-=1
		del self.idx[rem_obj]

		self.__bubbleDwn(i)
		return (rem_key,rem_obj)

	def remove_obj(self,obj):
		i=self.idx[obj]
		return self.__remove_idx(i)
	
	def update_key(self, new_key, obj):
		i=self.idx[obj]
		self.v[i]=(new_key,obj)
		#one of the two bubble will do nothing
		i=self.__bubbleUp(i)
		self.__bubbleDwn(i)
	def size(self):
		return self.size
	def __str__(self):
		return str(self.v)
	def __repr__(self):
		return self.__str__()

class HeapMax:
	"""
	Heap that keeps the maximum value at the top.
	This is implemented using the heapq module.
	"""
	def __init__(self):
		self.v=[]
	def push(self, key, obj):
		heapq.heappush(self.v,(-key,obj))
	def pop(self):
		key,obj=heapq.heappop(self.v)
		return (-key, obj)
	def top(self):
		key,obj=self.v[0]
		return (-key,obj)
	def size(self):
		return len(self.v)
	def __str__(self):
		return str(self.v)
	def __repr__(self):
		return self.__str__()

if __name__=='__main__':
	hm=HeapLookUp()
	
	hm.push(2,'c')
	hm.push(1,'a')
	hm.push(1,'b')
	hm.push(1.5,'d')
	hm.push(0.5,'e')

	hM=HeapMax()
	hM.push(2,'c')
	hM.push(1,'a')
	hM.push(1,'b')
	hM.push(1.5,'d')
	hM.push(0.5,'e')
	while hm.size>0:
		print "%s\t%s"%(hm.pop(),hM.pop())

