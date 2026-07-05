class TradingStrategy:

    @staticmethod
    def signal(
        rsi,
        ema20,
        ema50,
        macd,
        macd_signal,
        close,
        bb_upper,
        bb_lower
    ):

        # ==========================
        # TREND
        # ==========================
        bullish_trend = ema20 > ema50
        bearish_trend = ema20 < ema50

        # ==========================
        # BUY SIGNAL
        # ==========================
        if (
            bullish_trend and
            macd > macd_signal and
            45 <= rsi <= 65 and
            close <= (bb_lower * 1.02)
        ):

            return (
                "BUY",
                "Bullish trend + MACD confirmation + Pullback to lower Bollinger Band."
            )

        # ==========================
        # SELL SIGNAL
        # ==========================
        if (
            bearish_trend and
            macd < macd_signal and
            (
                rsi >= 70 or
                close >= (bb_upper * 0.98)
            )
        ):

            return (
                "SELL",
                "Bearish trend + MACD confirmation + Weak momentum."
            )

        # ==========================
        # EXIT LONG POSITION
        # ==========================
        if (
            macd < macd_signal and
            rsi > 70
        ):

            return (
                "SELL",
                "Take profit: Momentum is weakening."
            )

        # ==========================
        # HOLD
        # ==========================
        return (
            "HOLD",
            "No high-quality setup detected."
        )