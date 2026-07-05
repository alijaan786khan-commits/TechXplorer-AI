class TradingStrategy:

    @staticmethod
    def signal(rsi, ema20, ema50):

        # -------- TEST MODE --------
        # Force a SELL if RSI is above 50
        if rsi > 50:
            return "SELL", "TEST MODE: Forced SELL signal."

        # Otherwise force a BUY
        return "BUY", "TEST MODE: Forced BUY signal."