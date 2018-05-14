import ccxt
import pprint

def checker(exchange1, exchange2,symbol):


    print(type(symbol))

    # instantiating our exchanges        #getting min ask
    exchange1_name = exchange1  # storing the name of the exchange as a string
    exchange1 = getattr(ccxt, exchange1)
    exch1_inst = exchange1()
    exch1_inst.load_markets()

    exchange2_name = exchange2  # get max bid
    exchange2 = getattr(ccxt, exchange2)
    exch2_inst = exchange2()
    exch2_inst.load_markets()

    print(exchange1.currencies)
    pprint(exchange2.currencies)