class Node:
	def __init__(self, key, parent= None, left=None, right=None):
		self.key=key
		self.parent=parent
		self.left=left
		self.right=right
	def isRoot(self):
		return self.parent is None
	def isLeaf(self):
		return self.left is None and self.right is None
	def isLeftChild(self):
		if self.isRoot():
			return False
		return self.parent.left is self
	def isRightChild(self):
		if self.isRoot():
			return False
		return not self.__isLeftChild()
	def __str__(self):
		p='-' if self.parent is None else self.parent.key
		l='-' if self.left is None else self.left.key
		r='-' if self.right is None else self.right.key 
		return "(%s,%s,%s,%s)"%(self.key,p,l,r)
	def __repr__(self):
		return self.__str__()

class BST:
	"""Binary Search Tree"""

	def __init__(self):
		self.root=None
	
	def find(self, node, subtree):
		if subtree is None:
			return None
		if node.key==subtree.key:
			return subtree
		if node.key<subtree.key:
			return self.find(node, subtree.left)
		else:
			return self.find(node, subtree.right)
	
	def add(self, node):
		self.__add(node,self.root)
	
	def __add(self, node, subtree):
		if  self.root is None:
			self.root=node
		else:
			if node.key< subtree.key:
				if subtree.left is None:
					subtree.left=node
					node.parent=subtree
				else:
					self.__add(node, subtree.left)
			else:
				if subtree.right is None:
					subtree.right=node
					node.parent=subtree
				else:
					self.__add(node, subtree.right)
	
	def remove(self,node):
		cursor=self.find(node, self.root)
		if cursor is  None:
			return None

		#case 1
		if cursor.isLeaf():
			return self.__remove_leaf(cursor)
		#case 2 
		elif (cursor.left is None) != (cursor.right is None):
			#!= is like an XOR, ie only one of the two is true
			return self.__remove_single_branch(cursor)
		#case 3	
		else:
			return self.__remove_double_branch(cursor)
		


	def __remove_leaf(self, cursor):
		if cursor.isRoot():
			self.root=None
		else:
			if cursor.isLeftChild():
				cursor.parent.left=None
			else:
				cursor.parent.right=None
		return cursor

	def __remove_single_branch(self, cursor):
		if cursor.left is not None and cursor.right is None:
			if cursor.isRoot():
				self.root=cursor.left
			elif cursor.isLeftChild():
				cursor.parent.left=cursor.left
			else:
				cursor.parent.right=cursor.left
			cursor.left.parent=cursor.parent
		
		elif cursor.left is  None and cursor.right is not None:
			if cursor.isRoot():
				self.root=cursor.right
			elif cursor.isLeftChild():
				cursor.parent.left=cursor.right
			else:
				cursor.parent.right=cursor.right
			cursor.right.parent=cursor.parent
		
		return cursor

	def __remove_double_branch(self, cursor):
		predecessor=self.predecessor(cursor)
		#swap
		temp=cursor.key
		cursor.key=predecessor.key
		predecessor.key=temp

		if predecessor.isLeaf():
			self.__remove_leaf(predecessor)
		else:
			self.__remove_single_branch(predecessor)
		return predecessor

	def max(self, subtree):
		#just move ar right as you can
		if subtree.right is None:
			return subtree
		return self.max(subtree.right)

	def min(self, subtree):
		#just move as left as you can
		if subtree.left is None:
			return subtree
		return self.min(subtree.left)
	
	def predecessor(self, node):
		cursor=self.find(node, self.root)
		if cursor is  None:
			return None

		if cursor.left is not None:
			return self.max(cursor.left)
		else:
			cursorUp=cursor.parent
			while cursorUp is not None:
				if cursorUp.key < node.key:
					return cursorUp					
				cursorUp=cursorUp.parent
		return cursor
	
	def successor(self, node):
		cursor=self.find(node, self.root)
		if cursor is  None:
			return None

		if cursor.right is not None:
			return self.min(cursor.right)
		else:
			cursorUp=cursor.parent
			while cursorUp is not None:
				if cursorUp.key > node.key:
					return cursorUp					
				cursorUp=cursorUp.parent
		return cursor

	def traverse(self, order='in'):
		self.__traverse (self.root, order)
		 
	def __traverse(self,subtree, order):
		if subtree is None:
			return

		if order=='pre':
			print subtree

		self.__traverse(subtree.left, order)
		
		if order=='in':
			print subtree
		
		self.__traverse(subtree.right,order)
		
		if order=='post':
			print subtree
	@staticmethod
	def size(node):
		"""compute the size of the subtree whose root is node"""
		if node is None:
			return 0
		return 1+BST.size(node.left)+BST.size(node.right)

	def __str__(self):
		output=self.traverse(order='in')
		return output

if __name__=="__main__":
	t=BST()
	t.add(Node(10))
	t.add(Node(11))
	t.add(Node(5))
	t.add(Node(8))
	t.add(Node(4))
	t.add(Node(6))
	t.add(Node(6))
	t.add(Node(7))
	t.add(Node(3))
	print "size: ",BST.size(t.root)
	print "find 8",t.find(Node(8),t.root)
	print "find 6",t.find(Node(6),t.root)
	print "find 13",t.find(Node(13),t.root)
	print "max ",t.max(t.root)
	print "min ",t.min(t.root)
	print "predecessor 3",t.predecessor(Node(3))
	print "predecessor 4",t.predecessor(Node(4))
	print "predecessor 10",t.predecessor(Node(10))
	print "predecessor 5",t.predecessor(Node(5))
	print "successor 3",t.successor(Node(3))
	print "successor 4",t.successor(Node(4))
	print "successor 10",t.successor(Node(10))
	print "successor 5",t.successor(Node(5))
	print "remove ",t.remove(Node(4))
	t.traverse()
	print "remove ",t.remove(Node(5))	
	t.traverse()
	print "remove ",t.remove(Node(6))
	print "remove ",t.remove(Node(10))
	t.traverse()
	print "remove ",t.remove(Node(11))
	t.traverse()
	print "remove ",t.remove(Node(3))
	print "remove ",t.remove(Node(8))
	print "remove ",t.remove(Node(7))

	print "size: ",BST.size(t.root)
	