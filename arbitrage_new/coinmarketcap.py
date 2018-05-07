import json
import requests
import ccxt.async as ccxt


master_list=[] #this will contain all the currency pairs


#----------Now we will start to form lists of our pairs------------------------#

print(ccxt.exchanges)


class CurrencyPair:

	def __init__(self,name, exchange, bid, ask):
		self.name=name
		self.exchange=exchange
		self.bid=bid
		self.ask=ask



#GATEIO PAIRS

print(exchange.)

#master_list.append(gate_pairs_normalized)
#Gate pairs now contains any pairs we care about

'''''
#Bitstamp

request=requests.get(bitstamp)
data=request.json()

print("Loading Bitstamp Pairs...")

bitstamp_pairs=[]

for x in data:
	if("eur" not in str(x)):
		bitstamp_pairs.append(str(x["url_symbol"]))
master_list.append(bitstamp_pairs)

#Binance

request=requests.get(binance)
data=request.json()

print("Loading Binance Pairs...")

binance_pairs=[]

for x in data:
	binance_pairs.append(str(x["symbol"]))

master_list.append(binance_pairs)




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