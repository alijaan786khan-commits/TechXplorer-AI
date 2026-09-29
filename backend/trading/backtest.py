from exchange import ExchangeManager
from indicators import Indicators
from strategy import TradingStrategy
from backtester import Backtester

print("=" * 60)
print("🚀 TECHXPLORER AI BACKTEST STARTED")
print("=" * 60)
print("\nDownloading historical data from Binance (1H timeframe)...")

# Download historical data - 1H timeframe for better signals
exchange = ExchangeManager()

try:
    candles = exchange.get_ohlcv(
        "binance",
        "BTC/USDT",
        "1h",  # Changed from 5m to 1h
        500
    )
    print(f"✅ Downloaded {len(candles)} candles\n")
except Exception as e:
    print(f"❌ Error downloading data: {e}")
    exit(1)

# Calculate indicators
print("Calculating indicators...")
df = Indicators.calculate_indicators(candles)
print(f"✅ Indicators calculated\n")

# Create backtester
backtester = Backtester(100)

print("Running backtest on historical data...\n")

# Loop through historical candles
for idx, (_, row) in enumerate(df.iterrows()):
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

print(f"✅ Processed {idx + 1} candles\n")

# Print results
backtester.report()
