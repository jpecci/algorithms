import datetime as dt
from dateutil.parser import parse

def load_data(file):
	ans=[]
	with open(file) as fp:
		header=fp.next()
		for line in fp:
			sline=line.strip()
			if sline>0:
				#print sline
				ts,o,h,l,c,v,ac=sline.split(",")
				rec=(parse(ts),float(o),float(h),float(l),float(c),int(v),float(ac))
				ans.append(rec)

	return list(reversed(ans))

if __name__=="__main__":
	file="/Users/jacopo/Downloads/table.csv"
	data=load_data(file)