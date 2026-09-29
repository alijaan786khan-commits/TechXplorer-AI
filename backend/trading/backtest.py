from exchange import ExchangeManager
from indicators import Indicators
from strategy import TradingStrategy
from backtester import Backtester

# Download historical data
exchange = ExchangeManager()

candles = exchange.get_ohlcv(
    "binance",
    "BTC/USDT",
    "5m",
    500
)

# Calculate indicators

df = Indicators.calculate_indicators(candles)

# Create backtester
backtester = Backtester(100)

# Loop through historical candles
for _, row in df.iterrows():
    if row.isnull().any():
        continue

    signal, reason = TradingStrategy.signal(
        row["RSI"],
        row["EMA20"],
        row["EMA50"],
        row["EMA200"],
        row["MACD"],
        row["MACD_SIGNAL"],
        row["MACD_HIST"],
        row["close"],
        row["BB_UPPER"],
        row["BB_MIDDLE"],
        row["BB_LOWER"],
        row["ATR"],
        row["volume"],
        row["VOLUME_SMA"]
    )

    if signal == "BUY":
        backtester.buy(row["close"])
    elif signal == "SELL":
        backtester.sell(row["close"])

backtester.report()
