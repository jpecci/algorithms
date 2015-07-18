

def binary_search(v, s,e, value):
	if e==s:
		return -1
	elif e-s ==1:
		return s if v[s]== value else -1:
			
	mid=int((s+e)/2)

	if v[mid] < value:
		idx = binary_search(v,mid+1,e,value)
	elif v[mid] >value:
		idx = binary_search(v,s,mid,value)
	else:
		idx=mid 

	return idx

if __name__=='__main__':
	v=[1,4,6,7,8,10,11]
	v=[1,4,6]
	print binary_search(v,0,len(v),6)
