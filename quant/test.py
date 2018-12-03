# Python
import ccxt
import json
import time

#OHLCV structure
# 1504541580000, // UTC timestamp in milliseconds, integer
# 4235.4,        // (O)pen price, float
# 4240.6,        // (H)ighest price, float
# 4230.0,        // (L)owest price, float
# 4230.7,        // (C)losing price, float
# 37.72941911    // (V)olume (in terms of the base currency), float

exchange = ccxt.okcoinusd () # default id
okcoin1 = ccxt.okcoinusd ({ 'id': 'okcoin1' })
okcoin2 = ccxt.okcoinusd ({ 'id': 'okcoin2' })
id = 'btcchina'
btcchina = eval ('ccxt.%s ()' % id)
gdax = getattr (ccxt, 'gdax') ()

# from variable id
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
print exchange_class
print '--------'
exchange = exchange_class({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'timeout': 30000,
    'enableRateLimit': True,
})

print json.dumps(exchange.fetch_ticker('ETH/BTC')['info'],indent=4)
for item in exchange.fetchOHLCV('ETH/BTC', '1d'):
    ltime=time.localtime(int(str(item[0])[:-3]))
    timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    print timeStr
    print item
    print '------'

markets = exchange.load_markets()
# print json.dumps(markets, indent=4)
