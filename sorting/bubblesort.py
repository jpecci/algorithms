
def swap(a,i,j):
	temp=a[i]
	a[i]=a[j]
	a[j]=temp

def bubble_sort(a):
	for i in range(len(a)):
		swapped=False
		for j  in range(1, len(a)-i):
			if a[j-1]>a[j]:
				swap(a, j-1, j)
				swapped=True
			#print a
		if not swapped:
			break

if __name__=="__main__":
	v=[0,5,2,8,3,4,1]
	bubble_sort(v)
	print v