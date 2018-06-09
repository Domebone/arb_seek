import ccxt


def checker(exchange, symbol):

    exchange_name = exchange  # storing the name of the exchange as a string
    exchange = getattr(ccxt, exchange)
    exch_inst = exchange()
    exch_inst.load_markets()

    #hardcoding the list of exchanges without any module for wallet checking
    no_wallet_status=["tidex","therock","southxchange","quadrigacx","mixcoins","liqui","lakebtc","hitbtc","gemini","gateio",
                        "gatecoin","ethfinex","dsx","binance","bitlish","bitstamp","bitz","bl3p","btcmarkets","btcmarkets",
                        "ccex","cex","coinfloor","coingi","coinmate", "hadax", "bittrex", "cryptopia", "kraken"]


    idx = symbol.find('/')
    subs = symbol[:idx]

    out=True
    out1=True
    out2=True

  


    if (exchange_name =="coinexchange"):

        if exch_inst.currencies[subs]['info']['WalletStatus']=="online":
            out=True

    elif (exchange_name=="hitbtc2"):

        if(exch_inst.currencies[subs]['payin']):
            out1=True
        else:
            out1=False


        if (exch_inst.currencies[subs]['payout']):
            out2=True
        else:
            out2=False

        if out1 and out2:
            out=True
        else:
            out=False

    elif (exchange_name=="huobipro"):
        if(exch_inst.currencies[subs]['info']['deposit-enabled'] and exch_inst.currencies[subs]['info']['withdraw-enabled']):
            out=True
        else:
            out=False

    elif(exchange_name=="cobinhood"):
        if(exch_inst.currencies[subs]['info']['deposit_frozen'] and exch_inst.currencies[subs]['info']['withdrawal_frozen'] == False):
            out=True

        else:
            out=False

    elif (exchange_name=="kucoin"):
        if((exch_inst.currencies[subs]['info']["enableWithdraw"] and exch_inst.currencies[subs]['info']["enableDeposit"])):
            out=True
        else:
            out=False

    elif(exchange_name=="livecoin"):
        if (exch_inst.currencies[subs]['info']["walletStatus"]=="normal"):
            out=True
        else:
            out=False


    if exchange_name in no_wallet_status:
        print("No wallet data for " + exchange_name + " Check Manually.")

    elif out:
        print(exchange_name +" wallet online.")
    else:
        print(exchange_name+" wallet offline.")





