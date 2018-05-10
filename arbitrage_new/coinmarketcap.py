import json
import requests
import ccxt.async as ccxt
import asyncio
import time
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import RequestTimeout


startTime=time.time()

class CurrencyPair:									# Each unique Currency PAIR from each unique exchange will become an object

    def __init__(self, name, exchange, bid, ask):
        self.name = name
        self.exchange = exchange
        self.bid = bid
        self.ask = ask



# Our instance of our different exchanges will be held in a dict, indexed by exchange id.
exchanges = {}
symbols = []
rejectList= []
objectList= []
def getExchanges(exch):
    # looping through the exchanges to make dict of key and object pair
    rejectList = ['_1broker', 'allcoin', 'bibox', 'braziliex','btcx', 'coinegg',"coinmarketcap", 'coolcoin','huobicny', 'exx', 'ice3x',
                  'okcoinusd', 'okcoincny', 'wex', 'virwox', 'xbtce', 'vbtc', 'yunbi',"bibox", "bit2c","bitbank","bitbay"
                  ,"bitthumb"]
    #list of things we actually want to include
    inc_List=["coingi", "binance","bitlish","bitstamp","bittrex", "coinfloor","bl3p","btcmarkets","btcx","ccex",
              "cex","coinexchange","coinmate","dsx","ethfinex","gemini","hitbtc","hitbtc2",
              "kraken","kucoin","livecoin","quadrigacx","southxchange","tidex","therock","wex","mixcoins","liqui", "bitz",
              "cobinhood","gateio","gatecoin","hadax","huobipro","lakebtc"]

    #reading all exchanges
    for id in ccxt.exchanges:
        #ignoring all the ones we don't care about
        if id in inc_List and (id not in rejectList):
            #getting the id attribute for each
            exchange = getattr(ccxt, id)
            #building our dictionary of id and object pairs
            exch[id] = exchange()
    return exch

#change the global variable
exchanges= getExchanges(exchanges)

# some of the exchanges require API calls, delete those


async def loadInfo(exch):
    #loop though everyonbe of our exchanges
    for key in exch:
        print("Loading info from-> " +key+"\n...")
        #loading all the markets
        try:
            markets = await exch[key].load_markets()
        except Exception:
            pass


        #keeping the coins we have
        coins= exch[key].symbols
        symbols.append(coins)

        try:
            #geting all info and coins if we can
            if exch[key] is 'coinfloor': raise NotSupported
            t= await exch[key].fetch_tickers()
            for c in coins:
                stuff={}
                #checking that we got all the coins in our fetch tickers, sometimes our symbol fetch wont match the actual tickers
                if ((c in t) and ("CNY" not in c) and ("RUB" not in c) and ("/DOGE" not in c) and ("AUD" not in c) and ("PLN" not in c)
                    and ("GBP" not in c) and ("/WAVES" not in c) and ("WEUR" not in c) and ("WUSD" not in c)):
                    stuff = t[c]
                    #some exchanges have maxbid instead of regular bid
                    if 'maxbid' in stuff:
                        objectList.append(CurrencyPair(stuff['symbol'], key, stuff['maxbid'], stuff['maxask']))
                    else:
                        objectList.append(CurrencyPair(stuff['symbol'], key, stuff['bid'], stuff['ask']))
        except NotSupported:
            try:
                for x in coins:
                    if(("CNY" not in x) and ("RUB" not in x) and ("/DOGE" not in x) and ("AUD" not in x) and ("PLN" not in x)
                            and ("GBP" not in x) and ("/WAVES" not in x) and ("WEUR" not in x) and ("WUSD" not in x)):
                        t= await exch[key].fetch_ticker(x)
                    if 'maxbid' in t:
                        objectList.append(CurrencyPair(t['symbol'], key, t['maxbid'], t['maxask']))
                    else:
                        objectList.append(CurrencyPair(t['symbol'], key, t['bid'], t['ask']))
            except Exception:
                pass
        except Exception:
            pass

        #close our instances
        await exch[key].close()



print(exchanges)
#set up asyncio
loop= asyncio.get_event_loop()


loop.run_until_complete(loadInfo(exchanges))

#print(symbols)

loop.close()

#initializing our shit
currList=[]
currBidDic={}
currAskDic={}

#creating list of unique currencies
for obj in objectList:
    currList.append(obj.name)
currList= list(set(currList)) #set method will remove any duplicate currency pairs

#filling a dictionary of currencies to exchange and bids
for c in currList:
    currBidDic[c] = {}
    for o in objectList:
        if o.name == c:
            currBidDic[c][o.exchange]= o.bid
#filling our dic of currencies to exchange bids
for c in currList:
    currAskDic[c] = {}
    for o in objectList:
        if o.name == c:
            currAskDic[c][o.exchange]= o.ask

x= len(currAskDic)
to_be_deleted=[]
for b in iter(currBidDic):
    if len(currBidDic[b]) <=1 :to_be_deleted.append(b)
for t in to_be_deleted:
    del currBidDic[t]
    del currAskDic[t]

#for b in currBidDic:
    #min_bid=min(currBidDic[b].values())


    #print("Out of: ",currBidDic[b][0] ,"This is the min bid for: ",b,": ", min_bid)

#Getting the smallest
for b in currBidDic:

    max_bid = max(currBidDic[b].items())
    max_bid=max_bid[1]
    print(max_bid)



    min_ask= min(currAskDic[b].items())
    min_ask=min_ask[1]
    print(min_ask)
    if max_bid > 0:
        prof_calc=max_bid/min_ask
    min_bid_exch=""
    max_ask_exch=""

    for key,value in currBidDic[b].items():
        if value==max_bid:
            max_bid_exch=key

    for key, value in currAskDic[b].items():
        if value == min_ask:
            min_ask_exch = key

    print("Arbitrage opportunity of ", prof_calc,"for: ", b,"buy at: ",min_ask_exch ,"at price: ",min_ask," sell on: ",max_bid_exch, "for: ",max_bid)

print(currList)
print (currBidDic)
print (currAskDic)
print (x)
print (len(currAskDic))

runTime=time.time()-startTime
print(runTime)

'''
#--------------------------COMPARISON---------------------------------#
print("Master List: ")
for i in range(len(master_list)):
    print(master_list[i])

temp_list=[]

#we check all the matches

for i in range(len(master_list)):
    for j in range(len(master_list[i])):
        for k in range(len(master_list)):
            for l in range(len(master_list[k])):
                if ((master_list[i][j].lower()==master_list[k][l].lower()) and i != k):
                    if([i,j] not in index_list):
                        temp_list.append(i)
                        temp_list.append(j)
                        index_list.append(temp_list)	#we append the index of the matches
                        temp_list=[]
                    if([k,l] not in index_list):
                        temp_list.append(k)
                        temp_list.append(l)
                        index_list.append(temp_list)
                        temp_list=[]
                        print("Match!")


'''
