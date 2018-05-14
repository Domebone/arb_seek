from typing import Any, Union

import ccxt
from sub import coinmarketcapPriceFetch

bid_order_book={}
ask_order_book={}


def VolumeOptimize(exchange1,exchange2, symbol):  # go back to fetch order book for our arb op and check what volume is appropriate
    dollar_price=0
    if "JPY" not in symbol and "USD" not in symbol:
        dollar_price = coinmarketcapPriceFetch(symbol)
    if("USD" in symbol):
        dollar_price=1

    #initiating some vars
    ask_sum=0
    bid_sum=0
    length=0
    price_comp=0
    adjusted_first=[]
    adjusted_second=[]
    adjusted_third=[]
    adjusted_fourth=[]


    #instantiating our exchanges        #getting min ask
    exchange1_name=exchange1            #storing the name of the exchange as a string
    exchange1=getattr(ccxt, exchange1)
    exch1_inst=exchange1()

    exchange2_name = exchange2          #get max bid
    exchange2 = getattr(ccxt, exchange2)
    exch2_inst = exchange2()

    ask_order_book = exch1_inst.fetch_order_book(symbol,50)['asks']
    bid_order_book = exch2_inst.fetch_order_book(symbol,50)['bids']
    bid_length = len(bid_order_book)
    ask_length= len(ask_order_book)
    if bid_length>=ask_length:
        length=ask_length
    else:
        length=bid_length




    try:
        for i in range(0,length):
            ask_sum+=(ask_order_book[i][0]*ask_order_book[i][1])
            bid_sum += (bid_order_book[i][0] * bid_order_book[i][1])
            price_comp=bid_order_book[i][0]/ask_order_book[i][0]

            ask_dollar=dollar_price*ask_sum
            bid_dollar=dollar_price*bid_sum



            if (bid_dollar or ask_dollar)<100:
                adjusted_first.append(price_comp)



            if (bid_dollar or ask_dollar)<500 and (bid_dollar or ask_dollar)>=100:

                adjusted_second.append(price_comp)

            if (bid_dollar or ask_dollar)<1000 and (bid_dollar or ask_dollar)>=500:

                adjusted_third.append(price_comp)

            if (bid_dollar or ask_dollar)<5000 and (bid_dollar or ask_dollar)>=1000:

                adjusted_fourth.append(price_comp)





    except IndexError:
        print("Less than ", i , "orders. Investigate manually.")






