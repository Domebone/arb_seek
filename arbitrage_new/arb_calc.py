import json
import requests
import smtplib
import ccxt.async as ccxt
import asyncio
import time
import sys
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import RequestTimeout
from OrderBook_Calc import VolumeOptimize
from Wallet_Check import checker


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
    inc_List=["binance","ethfinex","kucoin","livecoin","ccex","coingi","bitlish","bitstamp","bittrex",
    "coinfloor","bl3p","btcmarkets","btcx"]
    '''  "cex","coinexchange","coinmate","dsx","gemini","hitbtc","hitbtc2",
              "kraken","quadrigacx","southxchange","tidex","therock","wex","mixcoins","liqui", "bitz",
              "cobinhood","gateio","gatecoin","hadax","huobipro","lakebtc","cryptopia"]'''

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
    #loop though everyone of our exchanges
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
                    and ("GBP" not in c) and ("/WAVES" not in c) and ("WEUR" not in c) and ("WUSD" not in c) and("BEE" not in c) and ("VRS") not in c)\
                        and ("AIO" not in c) and ("GET" not in c) and ("ATX" not in c) and ("ORE" not in c) and ("CNNC" not in c) and ("KURT" not in c) \
                        and ("KAYI" not in c) and ("VIDZ" not in c) and ("MYB" not in c) and ("OC" not in c) and ("CRC" not in c):
                    stuff = t[c]

                    #some exchanges have maxbid instead of regular bid
                    if ('maxbid' in stuff):

                        objectList.append(CurrencyPair(stuff['symbol'], key, stuff['maxbid'], stuff['maxask']))
                    else:
                        objectList.append(CurrencyPair(stuff['symbol'], key, stuff['bid'], stuff['ask']))
        except NotSupported:
            try:
                for x in coins:

                    if(("CNY" not in x) and ("RUB" not in x) and ("/DOGE" not in x) and ("AUD" not in x) and ("PLN" not in x)
                            and ("GBP" not in x) and ("/WAVES" not in x) and ("WEUR" not in x) and ("WUSD" not in x) and("BEE" not in x) and ("VRS") not in x)\
                            and ("AIO" not in x) and ("GET" not in x) and ("ATX" not in x) and ("ORE" not in x) and ("CNNC" not in x) and ("KURT" not in x)\
                            and ("KAYI" not in x) and ("VIDZ" not in x) and ("MYB" not in x) and ("OC" not in x) and ("CRC" not in x):
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



loop.close()

#initializing our shit
currList=[]
currBidDic={}
currAskDic={}

#creating list of unique currency names
for obj in objectList:
    currList.append(obj.name)
currList= list(set(currList)) #set method will remove any duplicate currency pairs

#filling a dictionary of currencies to exchange and bids
for c in currList:
    currBidDic[c] = {}
    for o in objectList:
        if o.name == c:         #so we go through our objectList, check for objects which have same name as our string and then get their bid price
            currBidDic[c][o.exchange]= o.bid
#filling our dic of currencies to exchange asks
for c in currList:
    currAskDic[c] = {}
    for o in objectList:        #same as our bidList
        if o.name == c:
            currAskDic[c][o.exchange]= o.ask


# in the end, for each currency we have a dict of tuples where we have exchange: bid or exchange:ask


to_be_deleted=[]
for b in iter(currBidDic):
    if len(currBidDic[b]) <=1 :to_be_deleted.append(b)          #we get rid of dict elements that only have one exchange
for t in to_be_deleted:                                         #this is to make sure we only look at coins that are on multiple exchanges
    del currBidDic[t]
    del currAskDic[t]



arbDic={}

for b in currBidDic:

    prof_calc=0

    #get max bid
    max_bid = max(currBidDic[b].items())    #this returns a tuple with the max and the exchange name
    max_bid=max_bid[1]                      #we use max_bid[1] to grab only the number value

    #get min
    min_ask= min(currAskDic[b].items())     #same for asks but we take the min because we want the lowest asking price
    min_ask=min_ask[1]

    if (min_ask is not None) and (max_bid is not None): #had some problems where min_ask or max_bid would be None
        if (min_ask > 0):                               #sometimes min_ask would be very low as well
            prof_calc=max_bid/min_ask                   #this is our actual arbitrage
    min_bid_exch=""
    max_ask_exch=""

    for key,value in currBidDic[b].items():             #we search for our exchange based on the value
        if value==max_bid:                              #i think we could in theory use max_bid[0] or min_ask[0]
            max_bid_exch=key

    for key, value in currAskDic[b].items():
        if value == min_ask:
            min_ask_exch = key







    # finding a return loop
    reverse_dict_ask = {}
    reverse_dict_bid = {}
    buying_exch = min_ask_exch
    selling_exch = max_bid_exch

    vol=0
    # only taking arb ops of 1.04 -1.2 to exclude anomalies from blocked wallets and mismatched names
    if (1.04 < prof_calc < 1.2):
        #print("prof calc OK")
        vol = VolumeOptimize(min_ask_exch, max_bid_exch, b)  # this checks what the optimal volume we should use is

        for o in objectList:

            if o.exchange == buying_exch:       #example: if you do MEME/BTC, to return, you only want BTC pairs and not LTC
                reverse_dict_bid[o.name]=o.bid  # each dict element will be equal to currency name : bid price (reverse of ask)

        for o in objectList:

            if o.exchange == selling_exch:
                idx = o.name.find('/')  # you only want to trade against the same base currency
                base1 = o.name[idx + 1:]
                idx = b.find('/')  # now we check our actual coin
                base2 = b[idx + 1:]
                if base1==base2:
                    reverse_dict_ask[o.name] = o.ask




        if vol>500:


            opp= "Arbitrage opportunity of ", prof_calc,"for: ", b,"buy at: ",min_ask_exch ,"at price: ",min_ask," sell on: ",max_bid_exch, "for: ",max_bid
            vol_test="This is profitable for "+ str(round(vol,2))+"$ and under"
            print(opp)
            print(vol_test)
            checker(max_bid_exch, b)
            checker(min_ask_exch, b)
            print("Return options: ")
            for r in reverse_dict_bid:
                for x in reverse_dict_ask:

                    if r ==x and (reverse_dict_ask[x] is not None) and  (reverse_dict_bid[r] is not None) :
                        ratio=reverse_dict_ask[x] / reverse_dict_bid[r]

                        if 1.01>ratio >.99:

                            print("Buy ", r, "on: ", selling_exch, "for ", reverse_dict_bid[r],"and sell on: ", buying_exch, "for", reverse_dict_ask[x])
                            print (ratio)


sys.stdout = open("~/Desktop/report.txt", "w")


"""""""""
content= 'egg'
mail =smtlib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login('arbitrageterry@gmail.com','m4r14n0p0l15')
mail.sendmail("arbitrageterry@gmail.com","arbitrageterry@gmail.com",content)
"""""

runTime=time.time()-startTime
print(runTime)

