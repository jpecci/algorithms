from collections import deque
from sets import Set

def bfs(graph, start):
	explored={} #store the distance
	queue=deque()
	queue.append(start)
	explored[start]=0
	while len(queue)>0:
		tail=queue.popleft()
		#print "%s -> "%(tail),
		for head, edge in graph.outBounds(tail).items():
			if  head not in explored:
				queue.append(head)
				explored[head]=explored[tail]+1
	return explored

def connected_components(graph):
	count_components=0
	components={}
	visited=Set() # this is across all the bfs calls
	for node in  graph:
		if node not in visited:
			# start a new bfs in this component
			count_components+=1
			components[count_components]=1
			queue=Queue() 
			queue.put(node)
			visited.add(node)
			while not queue.empty():
				v=queue.get()
				for w in graph[v]:
					if w not in visited:
						queue.put(w)
						visited.add(w)
						components[count_components]+=1
	return components

if __name__=='__main__':
	from graph import Graph, Edge, Vertex
	g=Graph()
	g.addEdge(Edge(Vertex('s'),Vertex('a')),False)
	
	g.addEdge(Edge(Vertex('b'), Vertex('s')),False)
	g.addEdge(Edge(Vertex('b'), Vertex('c')),False)
	 
	g.addEdge(Edge(Vertex('c'), Vertex('a')),False)
	g.addEdge(Edge(Vertex('c'), Vertex('d')),False)

	print "graph: \n",g

	start=Vertex('s')
	dist=bfs(g, start)
	print "dists:"
	for to in sorted(dist.items(), key=lambda p:p[1]):
		print "%s->%s: dist= %d"%(start,to[0],to[1])
	#print "components ",connected_components(g)
		
	
