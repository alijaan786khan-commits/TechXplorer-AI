import time
from datetime import datetime
from colorama import init, Fore
import pandas as pd
import numpy as np

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
risk = RiskManager(risk_percent=2.0)  # Increased to 2% risk per trade

print("=" * 60)
print("🚀 TECHXPLORER AI CRYPTO TRADING BOT STARTED")
print("=" * 60)
print("Downloading initial 500 candles to warm up indicators...\n")

# Warm up indicators with 500 candles
try:
    warmup_candles = exchange.get_ohlcv(
        "binance",
        "BTC/USDT",
        "1h",
        500
    )
    warmup_df = Indicators.calculate_indicators(warmup_candles)
    print(f"✅ Bot warmed up with 500 candles\n")
except Exception as e:
    print(f"Warning: Could not warm up: {e}\n")

while True:
    try:
        # ==========================
        # Download Market Data
        # ==========================
        candles = exchange.get_ohlcv(
            "binance",
            "BTC/USDT",
            "1h",
            200  # Increased from 100 to 200 for better EMA200 calculation
        )

        # ==========================
        # Calculate Indicators
        # ==========================
        df = Indicators.calculate_indicators(candles)
        latest = df.iloc[-1]

        # ==========================
        # NaN HANDLING - Skip if indicators are NaN
        # ==========================
        if pd.isna(latest["EMA200"]) or pd.isna(latest["MACD"]) or pd.isna(latest["RSI"]):
            print(f"\n{Fore.YELLOW}⏳ Warming up indicators... EMA200 still calculating")
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("Waiting 60 seconds...")
            time.sleep(60)
            continue

        # ==========================
        # Get Trading Signal
        # ==========================
        signal, reason = TradingStrategy.signal(
            latest["RSI"],
            latest["EMA20"],
            latest["EMA50"],
            latest["EMA200"],
            latest["MACD"],
            latest["MACD_SIGNAL"],
            latest["MACD_HIST"],
            latest["close"],
            latest["BB_UPPER"],
            latest["BB_MIDDLE"],
            latest["BB_LOWER"],
            latest["ATR"],
            latest["volume"],
            latest["VOLUME_SMA"]
        )

        # ==========================
        # Market Trend
        # ==========================
        trend = (
            "BULLISH"
            if latest["EMA20"] > latest["EMA50"]
            else "BEARISH"
        )

        # ==========================
        # Risk Management
        # ==========================
        risk_amount = risk.calculate_risk_amount(
            trader.balance
        )

        # ATR-based Stop Loss & Take Profit
        stop_loss = risk.calculate_stop_loss(
            latest["close"],
            latest["ATR"]
        )

        take_profit = risk.calculate_take_profit(
            latest["close"],
            latest["ATR"]
        )

        # ==========================
        # Execute Trade
        # ==========================
        if signal == "BUY":
            trader.buy(
                latest["close"],
                stop_loss,
                take_profit
            )

        elif signal == "SELL":
            trader.sell(
                latest["close"]
            )

        # Check Stop Loss / Take Profit
        trader.check_exit(
            latest["close"]
        )

        # ==========================
        # Statistics
        # ==========================
        stats = Statistics.get_stats()

        if stats["total"] > 0:
            win_rate = (
                stats["wins"] /
                stats["total"]
            ) * 100
        else:
            win_rate = 0

        # ==========================
        # Signal Color
        # ==========================
        if signal == "BUY":
            signal_color = Fore.GREEN
        elif signal == "SELL":
            signal_color = Fore.RED
        else:
            signal_color = Fore.YELLOW

        # ==========================
        # Display
        # ==========================
        print("\n" * 2)
        print("=" * 60)
        print("TECHXPLORER AI PAPER TRADING BOT")
        print("=" * 60)

        print(f"Time         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"BTC Price    : ${latest['close']:.2f}")

        print(f"\nTREND INDICATORS")
        print(f"EMA20        : ${latest['EMA20']:.2f}")
        print(f"EMA50        : ${latest['EMA50']:.2f}")
        print(f"EMA200       : ${latest['EMA200']:.2f}")

        print(f"\nMOMENTUM INDICATORS")
        print(f"MACD         : {latest['MACD']:.4f}")
        print(f"MACD SIGNAL  : {latest['MACD_SIGNAL']:.4f}")
        print(f"RSI          : {latest['RSI']:.2f}")

        print(f"\nVOLATILITY INDICATORS")
        print(f"BB UPPER     : ${latest['BB_UPPER']:.2f}")
        print(f"BB MIDDLE    : ${latest['BB_MIDDLE']:.2f}")
        print(f"BB LOWER     : ${latest['BB_LOWER']:.2f}")
        print(f"ATR          : ${latest['ATR']:.2f}")

        print(f"\nTREND         : {Fore.GREEN if trend == 'BULLISH' else Fore.RED}{trend}{Fore.RESET}")
        print(signal_color + f"SIGNAL       : {signal}")
        print(f"REASON       : {reason}")

        print(f"\nPOSITION INFO")
        print(f"BALANCE      : ${trader.balance:.2f}")
        print(f"POSITION     : {trader.position if trader.position else 'NONE'}")
        print(f"ENTRY PRICE  : ${trader.entry_price:.2f}")
        print(f"STOP LOSS    : ${trader.stop_loss:.2f}")
        print(f"TAKE PROFIT  : ${trader.take_profit:.2f}")
        print(f"RISK AMOUNT  : ${risk_amount:.2f}")

        print(f"\nTRADE STATISTICS")
        print(f"TOTAL TRADES : {stats['total']}")
        print(f"WINS         : {stats['wins']}")
        print(f"LOSSES       : {stats['losses']}")
        print(f"WIN RATE     : {win_rate:.2f}%")
        print(f"TOTAL PROFIT : ${stats['profit']:.2f}")

        print("=" * 60)
        print("Checking market again in 60 seconds...\n")

        time.sleep(60)

    except KeyboardInterrupt:
        print("\nBot stopped by user.")
        break

    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}")
        print("Retrying in 30 seconds...")
        time.sleep(30)
