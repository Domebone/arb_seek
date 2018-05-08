import json
import requests
import ccxt.async as ccxt
import asyncio
import time


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
def getExchanges(exch):
    # looping through the exchanges to make dict of key and object pair
    error_List = ['_1broker', 'allcoin', 'bibox', 'braziliex', 'coinegg', 'coolcoin', 'exx', 'huobicny', 'ice3x',
                  'okcoinusd', 'okcoincny', 'wex', 'virwox', 'xbtce', 'vbtc', 'yunbi',"cryptopia"]

    #reading all exchanges
    for id in ccxt.exchanges:
        #ignoring all the ones we don't care about
        if id not in error_List and (id not in rejectList):
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
        markets = await exch[key].load_markets()
        print(markets)

        #keeping the symbols and keys we have
        symbols.append(exch[key].symbols)
        #close our keys
        await exch[key].close()




print(exchanges)
#set up asyncio
loop= asyncio.get_event_loop()


loop.run_until_complete(loadInfo(exchanges))

print(symbols)

loop.close()


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
