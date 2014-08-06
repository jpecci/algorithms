import pandas.io.data as web
import datetime as dt
import numpy as np
import matplotlib.pylab as plt

BDAYS_PER_YEAR=250

FTSE100='^FTSE' #first 100
FTSE250='^FTMC' #from 101th to the 250th
FTSE350='^FTLC' #first 350
GILT=''
secs=[FTSE100, FTSE250]#,FTSE350]


lookback=0.5*365
today=dt.datetime.now().date()
start=today-dt.timedelta(days=lookback)

dfs=[]
vols=[]
for sec in  secs:
	df=web.DataReader(sec, 'yahoo', start, today)
	dfs.append(df)
	print ("%s: loaded %d samples from %s to %s")%(sec, len(df), df.index[0].date(), df.index[-1].date())
	df['ret']=df['Close']/df['Close'].shift()-1
	vol=np.sqrt(BDAYS_PER_YEAR*np.var(df['ret']))

	df['px']=df['Close']/vol
	delta=df['px'][0]-dfs[0]['px'][0]
	df['px']-=delta
	print ("vol=%.2f")%(100*vol)
	vols.append(vol)
	#df['px'].plot(label=sec)

#dfs[0]['px'].plot(subplots=True)
#dfs[1]['px'].plot(style='-o',grid=True)
plt.plot(dfs[1]['px']-dfs[0]['px'])
plt.show()
dates=set(dfs[0].index)
for df in dfs[1:]:
	dates=dates.intersection(df.index)
dates=sorted(dates)
print "%d dates from %s to %s"%(len(dates), dates[0].date(),dates[-1].date())

for i in xrange(1,len(dates)):
	if (dates[i]-dates[i-1]).days >2:
			print "%s %s"%(dates[i], dates[i-1])



