
class Node:
	def __init__(self, letter, value, num_children=256):
		self.parent=None
		self.letter=letter
		self.value=value
		self.children=[None]*num_children
	def __str__(self):
		num_children=len([c for c in self.children if c is not None])
		return "%s,%d,%d"%(self.letter,self.value,num_children)
	def __repr__(self):
		return self.__str__()
#----------
# REQUIRES SOME TESTING
#----------
class TrieTree:
	def __init__(self):
		self.root=Node("",0)
		self.size=0
	def add_word(self, word, tree):
		if len(word)<1:
			return
		letter=word[0]
		idx=ord(letter)
		if tree.children[idx] is None:
			tree.children[idx]=Node(letter,0)
		if len(word)==1:
			if tree.children[idx].value==0:
				self.size+=1 #increment only for new words
			tree.children[idx].value+=1 #frequency
		else:
			self.add_word(word[1:],tree.children[idx])
		
	def words_starting(self, prefix):
		cur=self.__find(prefix, self.root)
		if cur is None:
			return []
		return self.__get_words(cur,prefix)
	def __get_words(self, tree, pre_word):
		words=[]
		def helper(tree, pre_word):
			for child in tree.children:
				if child is not None:
					word=pre_word+child.letter
					if child.value>0:
						words.append(word)
					helper(child, word)
		helper(tree,pre_word)
		return words
	def __find(self, word, tree):
		if len(word)==0:
			return tree

		idx=ord(word[0])
		if len(word)==1:
			return tree.children[idx]
		else:
			if tree.children[idx] is None:
				return None
			return self.__find(word[1:], tree.children[idx])
	
	def get_value(self, word):
		node= self.__find(word, self.root)
		if node is None:
			return  0
		return node.value  

	def contains(self, word):
		node=self.__find(word, self.root)
		if node is None:
			return False
		return node.value>0

	def remove(self, word):
		node=self.__find(word, self.root)
		if node is not None:
			self.size-=node.value
			node.value=0

if __name__=='__main__':
	t=TrieTree()
	fp=open('/Users/jacopo/Downloads/alice_in_wonderland.txt','r')
	prune=["'",', '.', ';', '?', 's']
	count_words=0
	for line in fp:
		words=line.strip().split(" ")
		for word in words:
			for x in prune:
				if word.endswith(x):
					word=word[:-1]
			count_words+=1
			t.add_word(word, t.root)
	fp.close()
	words=t.words_starting("")
	swords=sorted(words,  key=lambda w:t.get_value(w))
	for sw in swords:
		print "%s %s"%(sw, t.get_value(sw))