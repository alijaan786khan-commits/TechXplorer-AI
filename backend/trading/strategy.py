"""
TechXplorer AI - Trading Strategy v2
Improved trend + momentum + volume strategy for higher quality entries.
"""


class TradingStrategy:
    """Improve signal quality to avoid noisy 5m false entries."""

    @staticmethod
    def signal(
        rsi,
        ema20,
        ema50,
        ema200,
        macd,
        macd_signal,
        macd_hist,
        close,
        bb_upper,
        bb_middle,
        bb_lower,
        atr,
        volume,
        volume_sma
    ):
        # Trend confirmation
        bullish_trend = ema20 > ema50 > ema200
        bearish_trend = ema20 < ema50 < ema200

        # Momentum confirmation
        macd_bullish = macd > macd_signal and macd_hist > 0
        macd_bearish = macd < macd_signal and macd_hist < 0
        macd_bullish_cross = macd > macd_signal and macd_hist > 0
        macd_bearish_cross = macd < macd_signal and macd_hist < 0

        # Volume confirmation
        volume_confirmed = volume >= (volume_sma * 0.85)

        # RSI zones
        rsi_buy_zone = 35 <= rsi <= 60
        rsi_sell_zone = 40 <= rsi <= 70
        rsi_strong_buy = rsi < 25
        rsi_strong_sell = rsi > 75

        # Price location relative to Bollinger Bands
        price_at_lower_band = close <= (bb_lower * 1.05)
        price_at_upper_band = close >= (bb_upper * 0.95)
        price_above_middle = close > bb_middle
        price_below_middle = close < bb_middle

        # =====================================
        # BUY LOGIC
        # =====================================
        bullish_breakout = (
            bullish_trend and
            macd_bullish and
            rsi_buy_zone and
            volume_confirmed and
            price_above_middle
        )

        bullish_pullback = (
            bullish_trend and
            macd_bullish and
            rsi_buy_zone and
            volume_confirmed and
            price_at_lower_band
        )

        bullish_reversal = (
            rsi_strong_buy and
            macd_bullish_cross and
            volume_confirmed and
            price_at_lower_band
        )

        if bullish_breakout:
            return (
                "BUY",
                "Bullish breakout: trend + MACD + RSI + volume confirmation"
            )

        if bullish_pullback:
            return (
                "BUY",
                "Bullish pullback: support bounce with strong momentum"
            )

        if bullish_reversal:
            return (
                "BUY",
                "Bullish reversal: oversold bounce with MACD confirmation"
            )

        # =====================================
        # SELL LOGIC
        # =====================================
        bearish_breakdown = (
            bearish_trend and
            macd_bearish and
            rsi_sell_zone and
            volume_confirmed and
            price_below_middle
        )

        overbought_exit = (
            rsi_strong_sell and
            macd_bearish_cross and
            volume_confirmed
        )

        trend_reversal = (
            ema20 < ema50 and
            macd_bearish and
            volume_confirmed
        )

        if bearish_breakdown:
            return (
                "SELL",
                "Bearish breakdown: downtrend + MACD + RSI + volume"
            )

        if overbought_exit:
            return (
                "SELL",
                "Overbought exit: strong bearish momentum with RSI rejection"
            )

        if trend_reversal:
            return (
                "SELL",
                "Trend reversal: EMA crossover with MACD confirmation"
            )

        return (
            "HOLD",
            "No high-quality setup. Waiting for better confirmation."
        )
