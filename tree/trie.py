
NUM_ASCII_CHARS=256

class Node:
	def __init__(self, letter, value):
		self.parent=None
		self.letter=letter #this is reduntant, just handy
		self.value=value
		self.children=[None]*NUM_ASCII_CHARS
	def __str__(self):
		num_children=len([c for c in self.children if c is not None])
		return "%s,%d,%d"%(self.letter,self.value,num_children)
	def __repr__(self):
		return self.__str__()
 
class TrieTree:
	def __init__(self):
		self.root=Node("",0)
		self.num_words=0

	def add_word(self, word):
		self.__add_word(word, self.root)
	
	def __add_word(self, word, tree):
		if len(word)<1:
			return
		letter=word[0]
		idx=ord(letter)
		#create the node if it doesnt exist
		if tree.children[idx] is None:
			tree.children[idx]=Node(letter,0)

		child=tree.children[idx]
		if len(word)==1:
			if child.value==0:
				self.num_words+=1 #increment only if new word
			child.value+=1 #frequency
		else:
			self.__add_word(word[1:], child)
		
	def words_starting(self, prefix):
		'''
		return a list of all the words with the prefix
		'''
		cursor=self.__find(prefix, self.root)
		if cursor is None:
			return []

		words=[]
		def helper(pre_word, tree):
			for child in tree.children:
				if child is not None:
					word=pre_word+child.letter
					if child.value>0:
						words.append(word)
					helper(word, child)

		helper(prefix, cursor)
		return words


	def __find(self, word, tree):
		'''return None if the word is not found'''
		if len(word)==0:
			return tree

		idx=ord(word[0])
		child=tree.children[idx]
		if len(word)==1:
			return child
		else:
			if child is None:
				return None
			return self.__find(word[1:], child)
	
	def get_value(self, word):
		node= self.__find(word, self.root)
		if node is None:
			return  -1
		return node.value  

	def contains(self, word):
		node=self.__find(word, self.root)
		if node is None:
			return False
		return node.value>0 #0 means this is only a prefix

	def remove(self, word):
		node=self.__find(word, self.root)
		if node is not None:
			if node.value >0: #decrement only if it was a word 
				self.num_words-=1
			node.value=0


if __name__=='__main__':
	t=TrieTree()
	fp=open('/Users/jacopo/Downloads/alice_in_wonderland.txt','r')
	prune=["'", ',', '.', ';', '?', '!' ,':', 's']
	count_words=0
	for line in fp:
		words=line.strip().split(" ")
		for word in words:
			for x in prune:
				if word.endswith(x):
					word=word[:-1]
			count_words+=1
			t.add_word(word)
	fp.close()
	words=t.words_starting("")
	swords=sorted(words,  key=lambda w:t.get_value(w))
	for sw in swords:
		print "%s %s"%(sw, t.get_value(sw))