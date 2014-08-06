class Node:
	def __init__(self, value, parent= None, left=None, right=None):
		self.value=value
		self.parent=parent
		self.left=left
		self.right=right
	def __str__(self):
		p='-' if self.parent is None else self.parent.value
		l='-' if self.left is None else self.left.value 
		r='-' if self.right is None else self.right.value 
		return "(%s,%s,%s,%s)"%(self.value,p,l,r)
	def __repr__(self):
		return self.__str__()

class BST:
	def __init__(self):
		self.root=None
	
	def find(self, node, subtree):
		if subtree is None:
			return None
		if node.value==subtree.value:
			return subtree
		if node.value<subtree.value:
			return self.find(node, subtree.left)
		else:
			return self.find(node, subtree.right)
	
	def add(self, node):
		self.__add(node,self.root)
	
	def __add(self, node, subtree):
		if  self.root is None:
			self.root=node
		else:
			if node.value< subtree.value:
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

	def remove_leaf(self, cursor):
		if cursor.value< cursor.parent.value:
			cursor.parent.left=None
		else:
			cursor.parent.right=None
	def remove_single_branch(self, cursor):
		if cursor.left is not None and cursor.right is  None:
			if cursor.value<cursor.parent.value:
				cursor.parent.left=cursor.left
			else:
				cursor.parent.right=cursor.left
			cursor.left.parent=cursor.parent
		elif cursor.left is  None and cursor.right is not None:
			if cursor.value<cursor.parent.value:
				cursor.parent.left=cursor.right
			else:
				cursor.parent.right=cursor.right
			cursor.right.parent=cursor.parent
	def remove_double_branch(self, cursor):
		predecessor=self.predecessor(cursor)
		self.swap(predecessor,cursor)
		if cursor.left is None and cursor.right is None:
			self.remove_leaf(cursor)
		else:
			self.remove_single_branch(cursor)

	def swap(self, node1, node2):
		print "swap is not working"
		temp=node1.parent
		node1.parent=node2.parent
		node2.paren=temp

		temp=node1.left
		node1.left=node2.left
		node2.left=temp

		temp=node1.right
		node1.right=node2.right
		node2.right=temp

	def remove(self,node):
		cursor=self.find(node, self.root)
		if cursor is  None:
			return None

		#case 1
		if cursor.left is None and cursor.right is None:
			self.remove_leaf(cursor)
		#case 2
		elif cursor.left is not None and cursor.right is  None:
			self.remove_single_branch(cursor)
		elif cursor.left is  None and cursor.right is not None:
			self.remove_single_branch(cursor)
		#case 3	
		else:
			self.remove_double_branch(cursor)
		return cursor

	def max(self, subtree):
		if subtree.right is None:
			return subtree
		return self.max(subtree.right)

	def min(self, subtree):
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
				if cursorUp.value < node.value:
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
				if cursorUp.value > node.value:
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

	def __str__(self):
		output=self.traverse_inorder()
		return output
if __name__=="__main__":
	t=BST()
	t.add(Node(10))
	t.add(Node(10))
	t.add(Node(5))
	t.add(Node(8))
	t.add(Node(4))
	t.add(Node(6))
	t.add(Node(6))
	t.add(Node(7))
	t.add(Node(3))
	print "find 8",t.find(Node(8),t.root)
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
	print "remove ",t.remove(Node(6))
	print "remove ",t.remove(Node(10))
	t.traverse()

	