import pandas as pd

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from ta.volatility import BollingerBands, AverageTrueRange


class Indicators:

    @staticmethod
    def calculate_indicators(candles):

        df = pd.DataFrame(
            candles,
            columns=[
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        )

        # RSI
        df["RSI"] = RSIIndicator(close=df["close"], window=14).rsi()

        # EMA
        df["EMA20"] = EMAIndicator(close=df["close"], window=20).ema_indicator()
        df["EMA50"] = EMAIndicator(close=df["close"], window=50).ema_indicator()
        df["EMA200"] = EMAIndicator(close=df["close"], window=200).ema_indicator()

        # MACD
        macd = MACD(close=df["close"])
        df["MACD"] = macd.macd()
        df["MACD_SIGNAL"] = macd.macd_signal()
        df["MACD_HIST"] = macd.macd_diff()

        # Bollinger Bands
        bb = BollingerBands(close=df["close"], window=20, window_dev=2)
        df["BB_UPPER"] = bb.bollinger_hband()
        df["BB_MIDDLE"] = bb.bollinger_mavg()
        df["BB_LOWER"] = bb.bollinger_lband()

        # ATR
        atr = AverageTrueRange(high=df["high"], low=df["low"], close=df["close"], window=14)
        df["ATR"] = atr.average_true_range()

        # Volume SMA
        df["VOLUME_SMA"] = df["volume"].rolling(window=20).mean()

        return df
