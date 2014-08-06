

def wis(ws):
	
	res=[None for w in ws]
	
	res[0]=ws[0]
	res[1]=max(ws[0], ws[1])

 	for i in xrange(2,len(ws)):
 		res[i]=max(res[i-1], res[i-2]+ws[i])
			
	return res 

def construct_sol(v,ws):
	#backward reconstruction
	sol=[]
	i=len(v)-1
	while i >1:	
		if v[i-1] > v[i-2] + ws[i]:
			# do not include
			i-=1
		else:
			sol.append(i)#include i
			i-=2
	sol.append(1 if ws[1]>ws[0] else 0)
	sol.reverse()
	return sol

if __name__=="__main__":
	ws=[1,4,5,4]
 	a= wis(ws)
 	print construct_sol(a,ws)