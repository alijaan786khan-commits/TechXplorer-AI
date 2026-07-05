import ccxt


class ExchangeManager:
    def __init__(self):
        # Binance
        self.binance = ccxt.binance({
            "enableRateLimit": True,
        })

        # MEXC
        self.mexc = ccxt.mexc({
            "enableRateLimit": True,
        })

    def get_price(self, exchange_name, symbol="BTC/USDT"):
        if exchange_name.lower() == "binance":
            ticker = self.binance.fetch_ticker(symbol)
        elif exchange_name.lower() == "mexc":
            ticker = self.mexc.fetch_ticker(symbol)
        else:
            raise ValueError("Unsupported exchange")

        return ticker["last"]
    