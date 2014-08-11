from util.heap import HeapLookUp
from util.general import time_func

def dkj_naive(graph, start):
	"""return the  distance from start to each other vertex.
	This function does not return the shorted paths
	Running time O(n*m)
	"""
	visited=set()
	visited.add(start)
	distances=dict([(v,99999999) for v in graph.vertexes])
	distances[start]=0
	prev_size_visited=len(visited)-1
	while prev_size_visited<len(visited):
		min_score=999999
		min_score_vertex=None
		for edge, (tail,head) in graph.edges.items():
			if tail in visited and head not in visited:
				#print "look at %s->%s"%(tail,head)
				score=distances[tail]+edge.length
				distances[head]=min(score, distances[head])
				if distances[head]<= min_score:
					min_score=distances[head]
					min_score_vertex=head
		 
		if min_score_vertex is not None:
			visited.add(min_score_vertex)
	return distances

def dkj_fast(graph, start):
	"""return the  distance from start to each other vertex.
	This function does not return the shorted paths
	Running time O(Nlog(N))
	"""
	 
	#add all the vertexes: the key represents the minimum
	#length to get to the vertex from any visited vertex
	not_visited=HeapLookUp()
	for v in graph.vertexes:
		edge=graph.getEdge(start, v)
		dist=99999999 if edge is None else edge.length		
		not_visited.push(dist, v)
	
	visited_dist={start:0}
	not_visited.remove_obj(start)

	while not_visited.size>0:
		
		dist, v=not_visited.pop() #heap returns the min
		visited_dist[v]=dist

		#update the not-visited vertexes reachable from v
		for head, edge in graph.outBounds(v).items():
			if not_visited.lookup(head) is not None:
				score =visited_dist[v] + edge.length
				old_score, head= not_visited.lookup(head)
				if score < old_score:
					not_visited.update_key(score, head)
	
	return visited_dist



if __name__=='__main__':
	from graph import Graph, Edge
	import  bfs, dfs 
	import random,time

	N=1000
	g=Graph()

	def create_vertexes(N):
		for x in xrange(N):
			g.addVertex(str(x))
		return list(g.vertexes.keys())


	def create_edges(N):
		for x in xrange(50*N):
			i=random.randint(0,N-1)
			j=random.randint(0,N-1)
			if i!=j \
		   		and not g.isConnected(vertexes[i],vertexes[j]) \
		   		and not g.isConnected(vertexes[j],vertexes[i]) :
				g.addEdge(Edge(random.randint(1,10)),vertexes[i],vertexes[j])
	 
	vertexes=time_func(create_vertexes,N)
	time_func(create_edges,N)

	time_func(bfs.bfs,g,vertexes[0])
	time_func(dfs.dfs,g,vertexes[0])
	time_func(dkj_fast,g,vertexes[0])
	time_func(dkj_naive,g,vertexes[0])
 	
 