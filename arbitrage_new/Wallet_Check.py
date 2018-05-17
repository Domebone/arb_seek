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



    if exchange_name in no_wallet_status:

        print("No wallet data for ",exchange_name, " Check Manually.")
    elif (exchange_name =="coinexchange"):


        print("Wallet status is: ", exch_inst.currencies[subs]['info']['WalletStatus'], "for coinexchange.")

    elif (exchange_name=="hitbtc2"):

        if(exch_inst.currencies[subs]['payin']):
            print("HitBtc2 deposit enabled")
        else:
            print("Hitbtc2 deposit disabled.")


        if (exch_inst.currencies[subs]['payout']):
            print("HitBtc2 withdrawal enabled")
        else:
            print("Hitbtc2 withdrawal disabled.")

    elif (exchange_name=="huobipro"):
        if(exch_inst.currencies[subs]['info']['deposit-enabled'] and exch_inst.currencies[subs]['info']['withdraw-enabled']):
            print("Huobipro wallet active")
        else:
            print("Huobipro wallet inactive.")

    elif(exchange_name=="cobinhood"):
        if(exch_inst.currencies[subs]['info']['deposit_frozen'] and exch_inst.currencies[subs]['info']['withdrawal_frozen'] == False):
            print("Cobinhood wallet inactive.")

        else:
            print("Cobinhood wallet active.")

    elif (exchange_name=="kucoin"):
        if((exch_inst.currencies[subs]['info']["enableWithdraw"] and exch_inst.currencies[subs]['info']["enableDeposit"])):
            print("Kucoin wallet active.")
        else:
            print("Kucoin wallet inactive.")

    elif(exchange_name=="livecoin"):
        if (exch_inst.currencies[subs]['info']["walletStatus"]=="normal"):
            print("Livecoin wallet active.")
        else:
            print("Livecoin wallet inactive.")
    else:


        print(exchange_name)
        print(exch_inst.currencies)





