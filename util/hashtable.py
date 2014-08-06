
class Entry:
	def __init__(self, key, value, next):
		self.key=key
		self.value=value
		self.next=next
		
	def __str__(self):
		return "(%s:%s)"%(self.key,self.value)

class HashTable:
	def __init__(self, capacity=16):
		self.v=[None]*capacity
		self.capacity=capacity
		self.size=0
		self.loadfactor=0.5
	def findPos(self, hashcode, capacity):
		return abs(hashcode)%capacity
	def add(self, key, value):
		pos=self.findPos(hash(key),self.capacity)
		if self.v[pos] is None:
			self.v[pos]=Entry(key,value,None)
			self.size+=1
			return None

		entry=self.v[pos]
		while entry is not None:
			if entry.key == key:
				old_value=entry.value
				entry.value=value
				return old_value
			entry=entry.next

		first_entry=self.v[pos]
		new_entry=Entry(key,value, first_entry)
		self.v[pos]=new_entry
		self.size+=1
		self.resize()
		return None		
		
	def get(self, key):
		pos=self.findPos(hash(key),self.capacity)
		if self.v[pos] is None:
			return None
		entry = self.v[pos]
		while entry is not None:
			if entry.key==key:
				return entry.value		
			entry=entry.next
		return None

	def remove(self, key):
		pos=self.findPos(hash(key),self.capacity)
		remove=False
		entry=self.v[pos]
		prev_entry=entry
		while entry is not None:
			if entry.key==key:
				remove=True
				break
			prev_entry=entry
			entry=entry.next
		if remove:
			self.size-=1
			if prev_entry is self.v[pos]:
				self.v[pos]=entry.next
			else:
				prev_entry.next=entry.next
			return entry
		return None

	def resize(self):
		if self.size > self.loadfactor*self.capacity:
			newCapacity=2*self.capacity
			print "resizing %d->%d..."%(self.capacity,newCapacity)
			self.capacity=newCapacity
			self.size=0
			temp=self.v
			self.v=[None]*newCapacity
			for row in temp:
				entry=row
				while entry is not None:
					self.add(entry.key, entry.value)
					entry=entry.next

	def __str__(self):
		output=""
		for entry in self.v:
			if entry is None:
				output+="None\n"
			else:
				while entry is not None:
					output+="%s "%entry
					entry=entry.next
				output+="\n"
		return output

if __name__=='__main__':
	h=HashTable(capacity=3)
	keys=['jaco', 'lucia', 'emma', 'joe', 'tony', 'jaco','emma','marco']
	values=range(len(keys))
	for k,v in zip(keys,values):
		print "add ",h.add(k,v)
