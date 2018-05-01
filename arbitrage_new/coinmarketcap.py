import json
import requests

#BaseTickerURLs
gateio="http://data.gate.io/api2/1/pairs"
bitstamp="https://www.bitstamp.net/api/v2/trading-pairs-info/"
binance="https://api.binance.com/api/v1/ticker/24hr"
liqui="https://api.liqui.io/api/3/info"
cryptopia="https://www.cryptopia.co.nz/api/GetCurrencies"
yobit="https://yobit.net/api/3/info"
coinExchange="https://www.coinexchange.io/api/v1/getmarkets"
hitBTC="https://api.hitbtc.com/api/2/public/currency"
gdax="https://api-public.sandbox.gdax.com/products"
gemini="https://api.gemini.com/v1/symbols"

master_list=[] #this will contain all the currency pairs
index_list=[]
#---------------------WE NOW HAVE PAIR URLs------------------------------------#
#----------Now we will start to form lists of our pairs------------------------#
#and("btc")and("eur")and("pln") and("pln") and ("cny")and ("jpy")


#GATEIO PAIRS

request=requests.get(gateio)
data=request.json()

print("Loading GateIO Pairs...")

gate_pairs=[]
gate_pairs_normalized=[]

for x in data:
	if("usdt" not in str(x)):
		gate_pairs.append(str(x))

for i in range(len(gate_pairs)):
	gate_pairs_normalized.append(gate_pairs[i].replace("_",""))

master_list.append(gate_pairs_normalized)
#Gate pairs now contains any pairs we care about

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


