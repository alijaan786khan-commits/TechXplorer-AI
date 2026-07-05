import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator


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

        df["RSI"] = RSIIndicator(
            close=df["close"],
            window=14
        ).rsi()

        df["EMA20"] = EMAIndicator(
            close=df["close"],
            window=20
        ).ema_indicator()

        df["EMA50"] = EMAIndicator(
            close=df["close"],
            window=50
        ).ema_indicator()

        return df