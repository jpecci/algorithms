import numpy as np
def swap(a,i,j):
	temp=a[i]
	a[i]=a[j]
	a[j]=temp

def naive_partition(a, idx_pivot):
	swap(a,0,idx_pivot)
	pivot=a[0]
	i=0
	j=len(a)-1
	res =np.zeros(len(a))
	for x  in a[1:]:
		if x <= pivot:
			res[i]=x
			i+=1
		else:
			res[j]=x
			j-=1
	res[i]=pivot
	return res

def partition(a, s, e):
	'''
	it partitions the vector a[s:e], i.e. it
 	puts the pivot element in the right position
	'''
	pivot=a[s] #the first element of the array
	j=s+1
	for i in range(s+1, e): 
		if a[i] <= pivot:
			swap(a,i,j) 
			j+=1
		else:
			pass
	#move pivot from s -> j-1
	i_pivot=j-1
	swap(a,s,i_pivot)
	return i_pivot

def quick_sort(a, s, e):
	'''
	sorts the vector a[s:e]
	'''
	if len(a[s:e])<=1:
		return #a 1-element vector is already sorted
	
	#print "pivot: ",a[s]
	i_pivot=partition(a, s, e)
	#print "partition ",a[s:e]
	quick_sort(a, s, i_pivot) #i_pivot is already in the right position
	quick_sort(a, i_pivot+1, e)


if  __name__=='__main__':
	import random
	import time
	from mergesort import merge_sort
	from bubblesort import bubble_sort
	#a=[3,8,2,5,1,4,7,6]
	v=[random.random() for x in xrange(1000000)]
	
	av=v[:]
	start=time.time()
	quick_sort(av,0,len(av))
	end=time.time()
	print "quick time: %.3f seconds"%(end-start)

	bv=v[:]
	start=time.time()
	merge_sort(bv)
	end=time.time()
	print "merge time: %.3f seconds"%(end-start)

	"""
	cv=v[:]
	start=time.time()
	bubble_sort(cv)
	end=time.time()
	print "time: %.3f seconds"%(end-start)
	"""