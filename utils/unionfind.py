

class UnionFind:
	def __init__(self):
		#the group is represented by the leading object
		#i.e. the one pointing at itself 
		self.objs={}
	
	def add(self, new_obj):
		"""add a new object to its own new group"""
		self.objs[new_obj]=new_obj
	
	def add2group(self, new_obj, group):
		"""add a new object to an existing group"""
		self.objs[new_obj]=group
	
	def merge_groups(self, obj1, obj2):
		"""merge two groups"""
		leader1=self.find_group(obj1)
		leader2=self.find_group(obj2)
		self.objs[leader1]=leader2
	
	
	def find_group(self, obj):
		"""find the group of an object 
		implements path compression
		"""
		path=[]
		o=obj
		leader=self.objs[o]
		while leader is not o:
			path.append(o)
			o=leader
			leader=self.objs[o]
		
		for o in path:
			self.objs[o]= leader
		return leader

	def __repr__(self):
		output=""
		for obj in self.objs:
			#output+="%s->%s\n"%(obj, self.objs[obj])
			output+="%s->%s\n"%(obj, self.find_group(obj))
		return output.strip()

if __name__=="__main__":
	uf=UnionFind()
	for o in "abcdefgh":
		uf.add(o)
		uf.merge_groups('a',o)
	print uf
	
	