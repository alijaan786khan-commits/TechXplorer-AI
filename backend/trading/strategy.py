"""
TechXplorer AI - Trading Strategy v3
Improved for 1H timeframe with better entry/exit logic.
"""


class TradingStrategy:
    """Optimized for 1H timeframe with cleaner signals."""

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
        # =====================================
        # TREND ANALYSIS
        # =====================================
        # Strong uptrend: EMA20 > EMA50 > EMA200
        strong_uptrend = ema20 > ema50 > ema200
        # Mild uptrend: EMA20 > EMA50 (ignore EMA200 for more signals)
        mild_uptrend = ema20 > ema50
        
        # Strong downtrend: EMA20 < EMA50 < EMA200
        strong_downtrend = ema20 < ema50 < ema200
        # Mild downtrend: EMA20 < EMA50
        mild_downtrend = ema20 < ema50

        # =====================================
        # MOMENTUM ANALYSIS
        # =====================================
        macd_bullish = macd > macd_signal
        macd_bearish = macd < macd_signal
        macd_bullish_cross = (macd > macd_signal) and (macd_hist > 0)
        macd_bearish_cross = (macd < macd_signal) and (macd_hist < 0)

        # =====================================
        # VOLUME ANALYSIS
        # =====================================
        # Accept if volume >= 80% of average (more relaxed)
        volume_confirmed = volume >= (volume_sma * 0.80) if volume_sma and volume_sma > 0 else True

        # =====================================
        # RSI ZONES
        # =====================================
        rsi_oversold = rsi < 35
        rsi_overbought = rsi > 65
        rsi_neutral = 40 <= rsi <= 60
        rsi_buy_zone = rsi < 50  # Relaxed: any RSI below 50 in uptrend
        rsi_sell_zone = rsi > 50  # Relaxed: any RSI above 50 in downtrend

        # =====================================
        # PRICE LOCATION
        # =====================================
        price_at_lower_band = close <= (bb_lower * 1.10)
        price_at_upper_band = close >= (bb_upper * 0.90)
        price_above_middle = close > bb_middle
        price_below_middle = close < bb_middle
        price_at_middle = abs(close - bb_middle) <= (atr * 0.5)

        # =====================================
        # BUY SIGNALS
        # =====================================
        
        # Signal 1: EMA Uptrend + MACD Bullish
        signal_1_buy = (
            mild_uptrend and
            macd_bullish and
            rsi_buy_zone and
            volume_confirmed
        )

        # Signal 2: Oversold Bounce (RSI < 35)
        signal_2_buy = (
            rsi_oversold and
            macd_bullish_cross and
            volume_confirmed and
            price_at_lower_band
        )

        # Signal 3: Pullback to Support
        signal_3_buy = (
            mild_uptrend and
            price_at_lower_band and
            rsi_buy_zone and
            volume_confirmed
        )

        # Signal 4: Price breaks above upper band with volume
        signal_4_buy = (
            mild_uptrend and
            close > bb_upper and
            volume_confirmed and
            rsi < 70
        )

        if signal_1_buy:
            return ("BUY", "Uptrend + MACD bullish + RSI confirmation")
        if signal_2_buy:
            return ("BUY", "Oversold bounce: RSI reversal at support")
        if signal_3_buy:
            return ("BUY", "Pullback to support in uptrend")
        if signal_4_buy:
            return ("BUY", "Breakout above resistance with volume")

        # =====================================
        # SELL SIGNALS
        # =====================================
        
        # Signal 1: EMA Downtrend + MACD Bearish
        signal_1_sell = (
            mild_downtrend and
            macd_bearish and
            rsi_sell_zone and
            volume_confirmed
        )

        # Signal 2: Overbought Rejection (RSI > 65)
        signal_2_sell = (
            rsi_overbought and
            macd_bearish_cross and
            volume_confirmed and
            price_at_upper_band
        )

        # Signal 3: Pullback to Resistance
        signal_3_sell = (
            mild_downtrend and
            price_at_upper_band and
            rsi_sell_zone and
            volume_confirmed
        )

        # Signal 4: Price breaks below lower band with volume
        signal_4_sell = (
            mild_downtrend and
            close < bb_lower and
            volume_confirmed and
            rsi > 30
        )

        if signal_1_sell:
            return ("SELL", "Downtrend + MACD bearish + RSI confirmation")
        if signal_2_sell:
            return ("SELL", "Overbought reversal: RSI rejection at resistance")
        if signal_3_sell:
            return ("SELL", "Pullback to resistance in downtrend")
        if signal_4_sell:
            return ("SELL", "Breakdown below support with volume")

        return (
            "HOLD",
            "No setup. Waiting for EMA/MACD alignment."
        )
