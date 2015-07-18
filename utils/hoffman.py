from heapq import *

class Node:
	def __init__(self, value, left, right):
		self.value=value
		self.left=left
		self.right=right
	def isLeaf(self):
		return self.left is None and self.right is None

def build_encoding_tree(words, probs):
	'''build the encoding tree organizing the words based on
	their probabilities'''
	heap= zip(probs, map(lambda w: Node(w,None, None), words))
	heapify(heap)

	while len(heap)>1:
		#select the two words with the smallest probabilities
		p_smallest, n_smallest=heappop(heap)
		p_2smallest, n_2smallest=heappop(heap)

		tree=Node(None, n_smallest, n_2smallest)
		tree_prob= p_smallest+ p_2smallest

		#insert the tree combining these two sub-trees
		heappush(heap, (tree_prob, tree))

	prob,tree=heappop(heap) #by now prob should be 1
	return tree

def build_codes(tree):
	"""given the encoding trees with all the words,
	build the codes"""
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
	from math import log,ceil

	words=['A',  'B',   'C', 'D', 'E']
	probs=[0.32, 0.25, 0.2, 0.18, 0.05]
	tree=build_encoding_tree(words, probs)
	codes=build_codes(tree)
	for word in words:
		print "%s %s"%(word, codes[word])
	

	average_len=0
	for word, prob in zip(words, probs):
		average_len+=prob*len(codes[word])
	std_len=ceil(log(len(words))/log(2)) #log base 2 of len(words)
	ratio=std_len/average_len
	print "average length: %.3f"%(average_len)
	print "compression ratio: %.3f"%ratio
