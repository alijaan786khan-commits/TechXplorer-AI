import time
from datetime import datetime
from colorama import init, Fore

from exchange import ExchangeManager
from indicators import Indicators
from strategy import TradingStrategy
from paper_trader import PaperTrader
from risk_manager import RiskManager

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

        # Open paper trade
        if signal == "BUY":
            trader.buy(
                latest["close"],
                stop_loss,
                take_profit
            )

        # Check if Stop Loss or Take Profit has been reached
        trader.check_exit(latest["close"])

        # Signal color
        signal_color = Fore.YELLOW

        if signal == "BUY":
            signal_color = Fore.GREEN
        elif signal == "SELL":
            signal_color = Fore.RED

        # Display information
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

        print("=" * 60)
        print("Checking market again in 30 seconds...")

        time.sleep(30)

    except KeyboardInterrupt:
        print("\nBot stopped.")
        break

    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(10)