import itertools as it
import  utils.timeutils as tu
import datetime as dt
from dateutil.parser import parse
import math
from stats import Sharpe, DrawDown, VAR


class Record(dict):
	fields=["ts","pnl"]
	@staticmethod
	def get_ts(line):
		return line.split(",",1)[0]
	def __init__(self,line): 
		tks=line.split(",")
		for i,(field,tk) in enumerate(zip(Record.fields, tks)):
			if i==0:
				self[field]=parse(tk)
			else:
				self[field]=float(tk)

def format_stats(stats):
	return "{start}-{end} {cpnl} {vol} {sharpe} {dd} {1dloss} {wdays} {var}".format(**stats)

def compute_pnl_stats(recs, capital):
	cpnl=0
	winning_days=0
	total_days=0
	max_1d_loss=0 #one day loss
	sharpe=Sharpe()
	dd=DrawDown()
	var=VAR()
	for i,rec in enumerate(recs):
		if i==0:
			start=rec['ts']
		total_days+=1
		winning_days+=1 if rec['pnl']>=0 else 0
		max_1d_loss = rec['pnl'] if rec['pnl']<max_1d_loss else max_1d_loss
		end=rec['ts']
		cpnl+=rec['pnl']
		ret=rec['pnl']/float(capital)
		sharpe.update(ret)
		dd.update(cpnl)
		var.update(rec['pnl'])
	return {'start':start.isoformat(), 'end':end.isoformat(), 'cpnl':cpnl, 'vol':sharpe.get_vol(), 
			"sharpe":sharpe.get(), 'dd':dd.get_deepest(), 'wdays':winning_days/float(total_days),
			'1dloss':max_1d_loss, 'var':(var.get(0.95),var.get_es(0.95))}	
def f():
	file="/Users/jacopo/tempj/dummy.py"
	with open(file) as fp:
		recs_all=[]
		for name, group in it.groupby(fp, lambda ln:parse(Record.get_ts(ln)).year):
			recs=[Record(line) for line in group]
			stats=compute_stats(recs, 5e6)
			print format_stats(stats)
			recs_all.append(recs)
	print ""
	stats=compute_stats(recs)
	print format_stats(stats)

if __name__=="__main__":
	from data import load_data
	file="/Users/jacopo/Downloads/table.csv"
	
	data=load_data(file)
	capital=data[0][4]
	px=[{'ts':data[i][0],'pnl':data[i][4]-data[i-1][4]} for i in xrange(1,len(data))]
	stats=compute_pnl_stats(px, capital)
	
	print stats

	