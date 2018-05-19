import json
import requests
import ccxt.async as ccxt
import asyncio
import functools
import time
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import RequestTimeout
from OrderBook_Calc import VolumeOptimize
from Wallet_Check import checker

inc_List = ["binance", "ethfinex", "kucoin", "livecoin", "ccex", "coingi", "bitlish", "bitstamp", "bittrex",
            "coinfloor", "bl3p", "btcmarkets", "btcx",
            "cex", "coinexchange", "coinmate", "dsx", "gemini", "hitbtc", "hitbtc2",
            "kraken", "quadrigacx", "southxchange", "tidex", "therock", "wex", "mixcoins", "liqui", "bitz",
            "cobinhood", "gateio", "gatecoin", "hadax", "huobipro", "lakebtc", "cryptopia"]
exchange = {}
symbols = []

#live laught love
async def get_exchanges(exch):
    for name in ccxt.exchanges:
        if name in inc_List:
            exchange_object = getattr(ccxt, name)
            exch[name] = exchange_object()
    asyncio.ensure_future(get_markets(exch))
    # return exch


async def get_markets(exch):
    print(exch)
    for key in exch:
        try:
            t = await exch[key].fetch_tickers()
            print(t)
        except NotSupported:
            pass


# async def runs(exch):
#   meth1=loop.create_task(get_exchanges(exch))
#  meth2=loop.create_task(get_markets(exch))
# await asyncio.wait([meth1,meth2])

loop = asyncio.get_event_loop()
loop.run_until_complete(get_exchanges(exchange))


#print(exchange)
#print(symbols)
