import ccxt


class ExchangeManager:
    def __init__(self):
        self.binance = ccxt.binance()
        self.mexc = ccxt.mexc()

    def get_price(self, exchange_name, symbol="BTC/USDT"):
        if exchange_name.lower() == "binance":
            ticker = self.binance.fetch_ticker(symbol)
        elif exchange_name.lower() == "mexc":
            ticker = self.mexc.fetch_ticker(symbol)
        else:
            raise ValueError("Unsupported exchange")

        return ticker["last"]

    def get_ohlcv(self, exchange_name, symbol="BTC/USDT", timeframe="5m", limit=100):
        if exchange_name.lower() == "binance":
            return self.binance.fetch_ohlcv(symbol, timeframe, limit=limit)
        elif exchange_name.lower() == "mexc":
            return self.mexc.fetch_ohlcv(symbol, timeframe, limit=limit)
        else:
            raise ValueError("Unsupported exchange")
