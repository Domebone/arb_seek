import requests
import json

#this converts our BASE into dollars

def coinmarketcapPriceFetch(symbol):

    idx = symbol.find('/')
    subs = symbol[idx+1:]

    id=""

    ListingsURL="https://api.coinmarketcap.com/v2/listings/"
    TickerURL="https://api.coinmarketcap.com/v2/ticker/"
    request=requests.get(ListingsURL)
    data=request.json()['data']

    for x in data:
        sym=x['symbol']

        if subs == sym and "JPY":

            id=x['id']

    TickerURL+=str(id)

    request=requests.get(TickerURL)
    data=request.json()['data']['quotes']['USD']    #sometimes throws a quotes exception

    price=data['price']

    return price


