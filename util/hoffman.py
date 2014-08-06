from heapq import *

class Node:
	def __init__(self, value, left, right):
		self.value=value
		self.left=left
		self.right=right
	def isLeaf(self):
		return self.left is None and self.right is None

def build_encoding_tree(words, prods):
	heap= zip(probs, map(lambda e: Node(e,None, None), words))
	heapify(heap)

	while len(heap)>1:
		p_smallest, n_smallest=heappop(heap)
		p_2smallest, n_2smallest=heappop(heap)

		tree=Node(None, n_smallest, n_2smallest)
		tree_prob= p_smallest+ p_2smallest

		heappush(heap, (tree_prob, tree))

	prob,tree=heappop(heap)
	return tree

def build_codes(tree):
	codes={}
	def helper(node, code):
		if node.isLeaf():
			codes[node.value]=code
		else:
			helper(node.left, code+"0")
			helper(node.right, code+"1")
	helper(tree, "")
	return codes

if __name__=='__main__':
	words=['A',  'B',   'C', 'D', 'E']
	probs=[0.32, 0.25, 0.2, 0.18, 0.05]
	tree=build_encoding_tree(words, probs)
	codes=build_codes(tree)
	for w in words:
		print "%s %s"%(w,codes[w])
	sum=0
	for w,prob in zip(words, probs):
		sum+=prob*1000*len(codes[w])

