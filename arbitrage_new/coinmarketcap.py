import json
import requests
import ccxt.async as ccxt
import asyncio
import time


# ----------Now we will start to form lists of our pairs------------------------#


class CurrencyPair:

    def __init__(self, name, exchange, bid, ask):
        self.name = name
        self.exchange = exchange
        self.bid = bid
        self.ask = ask



# a placeholder for your instances
exchanges = {}
symbols = []

def getExchanges(exch):
    # looping through the exchanges to make dict of key and object pair
    error_List = ['_1broker', 'allcoin', 'bibox', 'braziliex', 'coinegg', 'coolcoin', 'exx', 'huobicny', 'ice3x',
                  'okcoinusd', 'okcoincny', 'wex', 'virwox', 'xbtce', 'vbtc', 'yunbi']
    for id in ccxt.exchanges:
        if id not in error_List:
            exchange = getattr(ccxt, id)
            exch[id] = exchange()
            exch[id].close()

    '''for e in error_List:
        if e in exch:
            del exch[e]'''
    return exch

exchanges= getExchanges(exchanges)

#loop = asyncio.get_event_loop()
#loop.close()

# try 2
# some of the exchanges require API calls, delete those


async def getMarkets(exch):
    for key in exch:
        print(key)
        markets = await exch[key].load_markets()

        asyncio.sleep(.0000001)
        print(exch[key].symbols)
        symbols.append(exch[key].symbols)
        await exch[key].close()


#loop.run_until_complete(getExchanges(exchanges))



print(exchanges)

loop= asyncio.get_event_loop()


loop.run_until_complete(getMarkets(exchanges))

print(symbols)

loop.close()




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
