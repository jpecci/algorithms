
import math

class HeapPlus:
	"""
	this heap implementation contains a dictionary
	storing the index positions of the objects in the heap.
	This allows a constant time search as opposed to a log(N)
	as in the standard heap
	"""

	iTOP=1 #index of the first element, ie the minimum
	def __init__(self):
		self.v=[None] #exclude v[0] for semplicity
		self.idx={} #(obj:idx)
		self.size=0
	def __lastIndex(self):
		#last is not (size-1) since we start from index 1
		return self.size  

	def __parent(self,i):
		return int(math.floor(i/2))

	def __childL(self,i):
		return int(2*i)
	
	def __childR(self,i):
		return int(2*i+1)
	
	def __bubbleUp(self,i):
		 
		while i>HeapPlus.iTOP:
			key_child=self.v[i][0]
			i_parent=self.__parent(i)
			key_parent=self.v[i_parent][0]

			if key_child < key_parent:
				self.__swap(i, i_parent)
				i=i_parent
			else:
				break 
		return i
			
	def __bubbleDwn(self,i):
		
		while i<self.__lastIndex():
			key_parent=self.v[i][0]
			i_childL=self.__childL(i)
			if i_childL <=self.__lastIndex():
				i_child=i_childL
				i_childR=self.__childR(i)
				if i_childR<=self.__lastIndex():
					i_child= i_childL if self.v[i_childL][0]<self.v[i_childR][0] else i_childR
				key_child=self.v[i_child][0]
			
				if key_child < key_parent:
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

		#second  swap
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
		
	def get(self, obj):
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
	
	def updateKey(self, new_key, obj):
		i=self.idx[obj]
		self.v[i]=(new_key,obj)
		#one of the two bubble will do nothing
		i=self.__bubbleUp(i)
		self.__bubbleDwn(i)
	
	def __str__(self):
		return str(self.v)
	def __repr__(self):
		return self.__str__()

if __name__=='__main__':
	h=HeapPlus()
	h.push(2,'c')
	h.push(1,'a')
	h.push(1,'b')
	h.push(1.5,'d')
	h.push(0.5,'e')
	while h.size>0:
		print h.pop()

