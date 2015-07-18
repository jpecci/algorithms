import itertools as it

class Edge:
	id = 0
	def __init__(self,length):
		Edge.id+=1 #give and unique id
 		self.id=Edge.id
		self.length=length
	def __str__(self):
		return"<id=%s,len=%s>"%(self.id,self.length)
	def __repr__(self):
		return self.__str__()
	def __hash__(self):
		return hash(self.id)


class Graph:
	def __init__(self):
		#for each vetex store two dictionaries
		#the first is for the inbounds edges 
		#the second for the outbounds. Each item in the 
		#dictionary is of type (vertex:edge)
		self.vertexes={}
		#for each edge store (edge:(tail,head)) 
		self.edges={} 
	def addVertex(self, vertex):
		if vertex not in self.vertexes:
			self.vertexes[vertex]=(dict(),dict())
	def addEdge(self,edge, tail, head):
		if tail not in self.vertexes:
			self.addVertex(tail)
		if head not in self.vertexes:
			self.addVertex(head)

		self.vertexes[tail][1][head]=edge
		self.vertexes[head][0][tail]=edge
		self.edges[edge]=(tail,head)
		
	def getEdge(self, tail, head):
		return self.outBounds(tail).get(head, None)

	def removeEdge(self, edge):
		tail,head=self.edges[edge]
		del self.edges[edge]
		del self.outBounds(tail)[head]
		del self.inBounds(head)[tail] 	
	
	def removeVertex(self, vertex):
		for edge in it.chain(self.inBounds(vertex).values(), self.outBounds(vertex).values()):
			self.removeEdge(edge)
		del self.vertexes[vertex]

	def isConnected(self, tail, head):
		return self.getEdge(tail,head) is not None

	def outBounds(self, vertex):
		#return a dictionary
		return self.vertexes[vertex][1]
	
	def inBounds(self, vertex):
		#return a dictionary
		return self.vertexes[vertex][0]
	
	def __str__(self):
		output=""
		for vertex, (inBounds, outBounds) in self.vertexes.items():
			 
			output+="%s: IN"%(vertex)
			for tail, edge in inBounds.items():
				output+=" (%s:%s) "%(tail,edge)
			output+=" OUT"
			for head, edge in  outBounds.items():
				output+=" (%s:%s) "%(head,edge)
			output+="\n"
		for edge,ht in self.edges.items():
			output+="%s: %s\n"%(edge,ht)
		return output
	def __repr__(self):
		return self.__str__();


if __name__=='__main__':

	g=Graph()
	g.addVertex('s')
	g.addEdge(Edge(1),'a','s')
	g.addEdge(Edge(1),'s','a')
	g.addEdge(Edge(1),'s','b')
	g.addEdge(Edge(1),'b','a')
	g.addEdge(Edge(1),'s','c')
	print g.isConnected('a','s')
	print g.isConnected('a','c')
	#g.removeEdge(g.getEdge('b','a'))
	g.removeVertex('a')
	 
