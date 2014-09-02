
def find_a_sintex(graph):
	#sintex is a vertex with no outbound edges
	for v in graph.vertexes:
		if len(graph.outBounds(v))==0:
			return v
	return None

def topological_ordering(graph):
	ordering={}
 
	def helper(graph, sintex): 
		if len(graph.vertexes)==0:
			return 
	
		ordering[sintex]=len(graph.vertexes)
		graph.removeVertex(sintex)
		if len(graph.vertexes)>0:
			sintex=find_a_sintex(graph)
			if sintex is None:
				raise Exception("graph has a cycle")
			helper(graph, sintex)

	sintex=find_a_sintex(graph)
	if sintex is None:
		raise Exception("graph has a cycle")
	helper(graph, sintex)
	return ordering

if __name__=='__main__':
	from graph import Graph, Edge
	g=Graph()
	g.addVertex('s')
	g.addEdge(Edge(1),'a','s')
	#g.addEdge(Edge(1),'s','a')
	g.addEdge(Edge(1),'s','b')
	#g.addEdge(Edge(1),'b','a')
	g.addEdge(Edge(1),'s','c')

	ordering=topological_ordering(g)
	for v in sorted(ordering, key=lambda k:ordering[k]):
		print "%d %s"%(ordering[v],v)
