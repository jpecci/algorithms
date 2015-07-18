
import time
import datetime as dt
from odds import Odds
from utils.scheduler import Scheduler, Event
from data import callAPI

marketId=1.119521111
delay=1 #once every period seconds
fn="data.csv"
 
class Dump:
	def __init__(self, markertId, fn):
		self.cache=[]
		self.prev_dump=dt.datetime.now()

	def fetch_prices(self, marketId):
		ts=dt.datetime.now()
		market_book_req = '''{"marketIds":["%s"],
	                    "priceProjection":{"priceData":["EX_BEST_OFFERS"], "virtualise":"true"}}'''%(marketId)
		book=callAPI("listMarketBook", market_book_req)
		if book[0]['numberOfActiveRunners']!=2:
			raise Exception("numberOfActiveRunners = %s"%book[0]['numberOfActiveRunners'])

		get_price=lambda t: t[0]['price'] if t else None

		r1,r2=book[0]['runners']
		
		pt1=r1['lastPriceTraded']
		pt2=r2['lastPriceTraded']
		
		pb1=get_price(r1['ex']['availableToBack'])
		pb2=get_price(r2['ex']['availableToBack']) 
		
		pl1=get_price(r1['ex']['availableToLay'])
		pl2=get_price(r2['ex']['availableToLay'])
		curr=(ts, pb1, pl1, pt1, pt2, pb2, pl2)
		
		prev= self.cache[-1] if self.cache else (None,None)
		self.cache.append(curr)

		if curr[1:] != prev[1:]:
			print "{} R1:{}/{} ({}-{}) R2:{}/{}".format(*curr)


		if now-self.prev_dump > dt.timedelta(minutes=5):
			mode='a'  
			"""
			with open(fn, mode) as fp:
				for sample in self.cache:
					line="{}|{}|{}".format(*sample)
					fp.write(line+"\n")
			"""
			self.prev_dump=now
			self.cache=[]

dump=Dump(marketId, fn)
now=dt.datetime.now()
sc=Scheduler()
e=Event(now, dump.fetch_prices, marketId, dt.timedelta(seconds=1), now+dt.timedelta(minutes=10))
sc.register(e)
sc.run()