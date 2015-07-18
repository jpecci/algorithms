import requests
import json
import urllib2
import datetime as dt

SESSION_TOKEN="pqS80l3tZyN7QHvn9r0eGmMZzEz2E7p/nSG02g/KIBw="
APP_KEY="ngjLIbOBR0mopO7o"




ENDPOINT = "https://api.betfair.com/exchange/betting/rest/v1.0/"

HEADER={'X-Application' : APP_KEY, 
'X-Authentication' : SESSION_TOKEN ,
'content-type' : 'application/json' }

def callAPI(url_append, request):
    url=ENDPOINT+url_append+'/'
    response = requests.post(url, data=request, headers=HEADER)

    return json.loads(response.text)

if __name__=="__main__":
        

    #find live matches (aka events)
    #2=Tennis, 7742974=Wimbledon
    req_live_matches='''{"filter":{"eventTypeIds":["2"],
                          "competitionIds":["7742974"],
                          "inPlayOnly":true
                                  }           
                         }'''

    events=callAPI("listEvents",req_live_matches)
    for event in events:
        print "Id: {}, Name: {}, count={}".format(event['event']['id'],event['event']['name'],event['marketCount'])

    #select one event and fetch the 'Match Odds' market
    eventId=27483495
    mc_req = '''{"filter":{  "eventIds":["%s"] },
    		      "maxResults":"100",
    		      "marketProjection":["EVENT","RUNNER_METADATA"]
                  }'''%(eventId)
     
    markets=callAPI("listMarketCatalogue", mc_req)
    for market in markets:
        if market['marketName']=="Match Odds":
            print "{}: {}, id: {}".format(market['marketName'],market['event']['name'], market['marketId'])
            marketId=market['marketId']

    market_book_req = '''{"marketIds":["%s"], 
                        "priceProjection":{"priceData":["EX_BEST_OFFERS"]}}'''%(marketId)
    prev_ts=dt.datetime.now()
    for count in range(100):
        ts=dt.datetime.now()
        while ts-prev_ts < dt.timedelta(seconds=1):
            ts=dt.datetime.now()
        prev_ts=ts

        book=callAPI("listMarketBook", market_book_req)
        r1,r2=book[0]['runners']
        p1=r1['ex']['availableToBack'][0]['price']
        p2=r2['ex']['availableToBack'][0]['price']

        lpt1=r1['lastPriceTraded']
        lpt2=r2['lastPriceTraded']
        print "{} \t {}/{}".format(ts,p1,p2)