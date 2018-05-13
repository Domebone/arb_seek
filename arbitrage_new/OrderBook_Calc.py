from typing import Any, Union

import ccxt
from sub import coinmarketcapPriceFetch

bid_order_book={}
ask_order_book={}


def VolumeOptimize(exchange1,exchange2, symbol):  # go back to fetch order book for our arb op and check what volume is appropriate

    dollar_price = coinmarketcapPriceFetch(symbol)

    #initiating some vars
    ask_sum=0
    bid_sum=0
    length=0
    price_comp=0
    adjusted_first=[]
    adjusted_second=[]
    adjusted_third=[]
    adjusted_fourth=[]


    #instantiating our exchanges
    exchange1_name=exchange1
    exchange1=getattr(ccxt, exchange1)
    exch1_inst=exchange1()

    exchange2_name = exchange2
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






        if(len(adjusted_first)>0):

            sum1=sum(adjusted_first)/len(adjusted_first)
            if(sum1>1.1):
                print("With 100$ or less you have the following arbitrage: ", sum1)
        else: print("Volume is high enough that you can use more than 100$ and be profitable")
        if(len(adjusted_second)>0):
            sum2 = sum(adjusted_second) / len(adjusted_second)
            if (sum2>1.1):

                print("With 500$ or less you have the following arbitrage: ", sum2)
            else: print("With 100-500$, arbitrage drops below 10% profit")
        else: print("If youre using 100-500$, check order books Manually")
        if(len(adjusted_third)>0):
            sum3 = sum(adjusted_third) / len(adjusted_third)
            if(sum3>1.1):

                print("With 1000$ or less you have the following arbitrage: ", sum3)
            else: print("With 500-1000$, arbitrage drops below 10% profit")
        else:print("Check Data between 500-1000$ Manually")
        if(len(adjusted_fourth)>0):
            sum4 = sum(adjusted_fourth) / len(adjusted_fourth)
            if (sum4>1.1):

                print("With 5000$ or less you have the following arbitrage: ", sum4)
            else: print("Between 1000-5000$, arbitrage drops below 10% profit")
        else: print("No arb ops between 1000-5000$ or not enough data from exchange. Verify Manually")


    except IndexError:
        print("Less than ", i , "orders. Investigate manually.")






