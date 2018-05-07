import json
import requests
import ccxt
import asyncio
import ccxt


master_list=[] #this will contain all the currency pairs


#----------Now we will start to form lists of our pairs------------------------#

#print(ccxt.exchanges)


class CurrencyPair:

	def __init__(self,name, exchange, bid, ask):
		self.name=name
		self.exchange=exchange
		self.bid=bid
		self.ask=ask


# a placeholder for your instances
exchanges = {}

#looping through the exchanges to make dict of key and objext pair
for id in ccxt.exchanges:
	exchange = getattr(ccxt, id)
	exchanges[id] = exchange()

#try 2
#some of the exchanges require API calls, delete those
error_List= ['_1broker', 'allcoin', 'bibox', 'braziliex', 'coinegg', 'coolcoin', 'exx', 'huobicny','ice3x', 'okcoinusd', 'okcoincny', 'wex', 'virwox', 'xbtce', 'vbtc','yunbi']
for e in error_List:
	del exchanges[e]

print(exchanges)
for key in exchanges:
	print ( key, exchanges[key].load_markets())

'''
async def getticker():
    exchange = ccxt.okex({'proxy': 'https://cors-anywhere.herokuapp.com/'})  # ←------- added proxy here
    ticker = await exchange.fetch_ticker('BTC/USDT')
    await exchange.close()
    print(ticker)

asyncio.get_event_loop().run_until_complete(getticker())
>>>>>>> origin/master

'''''

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