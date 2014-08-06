from heapplus import HeapPlus

def dkj_naive(graph, start):
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
				new_dist=distances[tail]+edge.length
				distances[head]=min(new_dist, distances[head])
				if distances[head]<= min_score:
					min_score=distances[head]
					min_score_vertex=head
		 
		prev_size_visited=len(visited)
		if min_score_vertex is not None:
			#print "added ",min_score_vertex
			visited.add(min_score_vertex)
	return distances

def dkj_fast(graph, start):
	 
	not_visited_vertexes=HeapPlus()
	for v in graph.vertexes:
		edge=graph.getEdge(start, v)
		dist=99999999 if edge is None else edge.length		
		not_visited_vertexes.add(dist, v)
	
	visited_distances={}
	visited_distances[start]=0
	not_visited_vertexes.remove_obj(start)

	while not_visited_vertexes.size>0:
		
		dist,vertex=not_visited_vertexes.pop() #heap returns the min
		visited_distances[vertex]=dist
		
		for head,edge in graph.outBounds(vertex).items():
			if not_visited_vertexes.get(head) is not None:
				new_dist =visited_distances[vertex]+edge.length
				old_dist, head= not_visited_vertexes.get(head)
				if new_dist < old_dist:
					not_visited_vertexes.updateKey(new_dist, head)
	
	return visited_distances


def run_and_time(name,f,*args):
	print "%s running..."%name
	start=time.time()
	res=f(*args)
	end=time.time()
	print "\tfinished in %.4f mins"%( (end-start)/60.)
	return res

if __name__=='__main__':
	from graph import Graph, Edge
	import  bfs, dfs 
	import random,time

	N=1000000
	g=Graph()

	def create_vertexes(N):
		for x in xrange(N):
			g.addVertex(str(x))
		return list(g.vertexes.keys())

	vertexes=run_and_time("created_vertexes",create_vertexes,N)

	def create_edges(N):
		for x in xrange(50*N):
			i=random.randint(0,N-1)
			j=random.randint(0,N-1)
			if i!=j \
		   		and not g.isConnected(vertexes[i],vertexes[j]) \
		   		and not g.isConnected(vertexes[j],vertexes[i]) :
				g.addEdge(Edge(random.randint(1,10)),vertexes[i],vertexes[j])
	 
	run_and_time("create_edges",create_edges,N)

	v_start=vertexes[0]
	
	hoops = run_and_time("bfs",bfs.bfs,g,v_start)
	run_and_time("dfs",dfs.dfs,g,v_start)
	 
	dists_fast=run_and_time("dkj_fast",dkj_fast,g,v_start)
 	#dists_naive=run_and_time("dkj_naive",dkj_naive,g,v_start)

	keys_sorted=sorted(dists_fast, key=lambda x:dists_fast[x])
	for k in keys_sorted[:10]:
		print "to: %s lenF: %s hoops:%s"%(k, dists_fast[k],hoops.get(k))
	print ""
	for k in keys_sorted[-10:]:
		print "to: %s lenF: %s hoops:%s"%(k, dists_fast[k],hoops.get(k))