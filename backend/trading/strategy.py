class TradingStrategy:

    # Turn this on only for testing
    TEST_MODE = True

    @staticmethod
    def signal(rsi, ema20, ema50):

        # Force one BUY signal
        if TradingStrategy.TEST_MODE:
            TradingStrategy.TEST_MODE = False
            return "BUY", "TEST MODE: Forced BUY signal."

        # Normal strategy
        if rsi < 30 and ema20 > ema50:
            return "BUY", "Oversold market in an uptrend."

        elif rsi > 70 and ema20 < ema50:
            return "SELL", "Overbought market in a downtrend."

        elif ema20 > ema50:
            return "HOLD", "Bullish trend detected. Wait for a better entry."

        elif ema20 < ema50:
            return "HOLD", "Bearish trend detected. Wait for confirmation."

        return "HOLD", "No clear signal."