import requests
import json

#this converts our BASE into dollars

def coinmarketcapPriceFetch(symbol):

    idx = symbol.find('/')
    subs = symbol[idx+1:]
    price=0
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
    try:
        data=request.json()['data']['quotes']['USD']
        price = data['price']                           #sometimes throws a quotes exception
    except KeyError:
        pass


    return price


