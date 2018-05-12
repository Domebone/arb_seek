import ccxt
from sub import coinmarketcapPriceFetch

bid_order_book={}
ask_order_book={}


def VolumeOptimize(exchange1,exchange2 ,type, symbol):  # go back to fetch order book for our arb op and check what volume is appropriate

    dollar_price = coinmarketcapPriceFetch(symbol)

    #initiating some vars
    vol_sum = 0
    adj_price = 0
    length=0

    #instantiating our exchanges
    exchange1_name=exchange1
    exchange1=getattr(ccxt, exchange1)
    exch1_inst=exchange1()
    exchange2_name = exchange2
    exchange2 = getattr(ccxt, exchange2)
    exch2_inst = exchange2()

    ask_order_book = exch1_inst.fetch_order_book(symbol)['asks']
    if (len(ask_order_book)>20):
        length=20
    else:
        length=len(ask_order_book)
    for i in range(0,length):   #sum of volume
        vol_sum=vol_sum+ask_order_book[i][1]
    for i in range(0,length):   #weighted average
        adj_price=adj_price+((ask_order_book[i][1]/vol_sum)*ask_order_book[i][0])
    print("Asks for: ", symbol, " on ",exchange_name,": ",ask_order_book)
    print ("Adjusted ask price: ", adj_price, " for ",vol_sum," coins.")

    bid_order_book = exch_inst.fetch_order_book(symbol)['bids']
    if (len(bid_order_book)>20):
        length=20
    else:
        length=len(bid_order_book)
    for i in range(0, length):  # sum of volume
        vol_sum = vol_sum + bid_order_book[i][1]
    for i in range(0, length):  # weighted average
        adj_price = adj_price + ((bid_order_book[i][1] / vol_sum) * bid_order_book[i][0])
    print("Bids for: ", symbol, " on ", exchange_name, ": ", bid_order_book)
    print("Adjusted bid price: ", adj_price, " for ", vol_sum, " coins.")