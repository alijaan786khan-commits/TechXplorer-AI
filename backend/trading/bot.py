import time
from datetime import datetime
from colorama import init, Fore

from exchange import ExchangeManager
from indicators import Indicators
from strategy import TradingStrategy
from paper_trader import PaperTrader
from risk_manager import RiskManager
from trade_statistics import Statistics

# Initialize colorama
init(autoreset=True)

# Create objects
exchange = ExchangeManager()
trader = PaperTrader()
risk = RiskManager()

print("=" * 60)
print("🚀 TECHXPLORER AI CRYPTO TRADING BOT STARTED")
print("=" * 60)

while True:
    try:
        # Download market data
        candles = exchange.get_ohlcv("binance", "BTC/USDT", "5m", 100)

        # Calculate indicators
        df = Indicators.calculate_indicators(candles)
        latest = df.iloc[-1]

        # Get trading signal
        signal, reason = TradingStrategy.signal(
            latest["RSI"],
            latest["EMA20"],
            latest["EMA50"]
        )

        # Market trend
        trend = "BULLISH" if latest["EMA20"] > latest["EMA50"] else "BEARISH"

        # Risk calculations
        risk_amount = risk.calculate_risk_amount(trader.balance)
        stop_loss = risk.calculate_stop_loss(latest["close"])
        take_profit = risk.calculate_take_profit(latest["close"])

        # ==========================
        # Execute Trades
        # ==========================

        if signal == "BUY":
            trader.buy(
                latest["close"],
                stop_loss,
                take_profit
            )

        elif signal == "SELL":
            trader.sell(latest["close"])

        # Check Stop Loss / Take Profit
        trader.check_exit(latest["close"])

        # Signal color
        if signal == "BUY":
            signal_color = Fore.GREEN
        elif signal == "SELL":
            signal_color = Fore.RED
        else:
            signal_color = Fore.YELLOW

        # Get Statistics
        stats = Statistics.get_stats()

        if stats["total"] > 0:
            win_rate = (stats["wins"] / stats["total"]) * 100
        else:
            win_rate = 0

        # Display
        print("\n" * 2)
        print("=" * 60)
        print("TECHXPLORER AI PAPER TRADING BOT")
        print("=" * 60)

        print(f"Time         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"BTC Price    : {latest['close']:.2f}")
        print(f"EMA20        : {latest['EMA20']:.2f}")
        print(f"EMA50        : {latest['EMA50']:.2f}")
        print(f"TREND        : {trend}")
        print(f"RSI          : {latest['RSI']:.2f}")

        print(signal_color + f"SIGNAL       : {signal}")
        print(f"REASON       : {reason}")

        print(f"BALANCE      : ${trader.balance:.2f}")
        print(f"POSITION     : {trader.position}")
        print(f"ENTRY PRICE  : {trader.entry_price:.2f}")
        print(f"STOP LOSS    : {trader.stop_loss:.2f}")
        print(f"TAKE PROFIT  : {trader.take_profit:.2f}")
        print(f"RISK AMOUNT  : ${risk_amount:.2f}")

        print("\nTRADE STATISTICS")
        print(f"TOTAL TRADES : {stats['total']}")
        print(f"WINS         : {stats['wins']}")
        print(f"LOSSES       : {stats['losses']}")
        print(f"WIN RATE     : {win_rate:.2f}%")
        print(f"TOTAL PROFIT : ${stats['profit']:.2f}")

        print("=" * 60)
        print("Checking market again in 30 seconds...")

        time.sleep(30)

    except KeyboardInterrupt:
        print("\nBot stopped.")
        break

    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(10)