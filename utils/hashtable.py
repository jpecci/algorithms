
class Entry:
	def __init__(self, key, value, next):
		self.key=key
		self.value=value
		self.next=next
		
	def __str__(self):
		return "(%s:%s)"%(self.key,self.value)

class HashTable:
	def __init__(self, capacity=16):
		self.buckets=[None]*capacity
		self.capacity=capacity
		self.size=0
		self.loadfactor=0.5

	def __hash2pos(self, hashcode):
		return abs(hashcode)%self.capacity
	
	def add(self, key, value):
		pos=self.__hash2pos(hash(key))
		if self.buckets[pos] is None:
			self.buckets[pos]=Entry(key,value,None)
			self.size+=1
			return None

		#scroll throught the bucket to update
		entry=self.buckets[pos]
		while entry is not None:
			if entry.key == key:
				old_value=entry.value
				entry.value=value
				return old_value
			entry=entry.next

		#append at the front
		first_entry=self.buckets[pos]
		new_entry=Entry(key,value, first_entry)
		self.buckets[pos]=new_entry
		self.size+=1
		self.__resize()
		return None		
		
	def get_value(self, key):
		pos=self.__has2pos(hash(key))
		if self.buckets[pos] is None:
			return None

		#scroll throught the bucket
		entry = self.buckets[pos]
		while entry is not None:
			if entry.key==key:
				return entry.value		
			entry=entry.next
		return None

	def remove_entry(self, key):
		pos=self.__has2pos(hash(key))
		remove=False
		cursor=self.buckets[pos]
		prev_cur=cursor
		while cursor is not None:
			if cursor.key==key:
				remove=True
				break
			prev_cur=cursor
			cursor=cursor.next
		if remove:
			self.size-=1
			if prev_cur is self.buckets[pos]:
				self.buckets[pos]=cursor.next
			else:
				prev_cur.next=cursor.next
			return cursor
		return None

	def __resize(self):
		if self.size > self.loadfactor*self.capacity:
			self.capacity*=2
			#print "resizing %d->%d..."%(self.capacity,newCapacity)
			self.size=0
			temp=self.buckets
			self.buckets=[None]*self.capacity
			for bucket in temp:
				entry=bucket
				while entry is not None:
					self.add(entry.key, entry.value)
					entry=entry.next

	def __str__(self):
		output=""
		for bucket in self.buckets:
			entry=bucket
			if entry is None:
				output+="None\n"
			else:
				while entry is not None:
					output+="%s "%entry
					entry=entry.next
				output+="\n"
		return output
	def __repr__(self):
		return self.__str__()

if __name__=='__main__':
	h=HashTable(capacity=3)
	keys=['jaco', 'lucia', 'emma', 'joe', 'tony', 'jaco','emma','marco']
	values=range(len(keys))
	for k,v in zip(keys,values):
		print "add ",h.add(k,v)
