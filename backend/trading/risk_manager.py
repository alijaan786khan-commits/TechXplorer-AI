class RiskManager:

    def __init__(
        self,
        risk_percent=2.0,  # Increased from 1.0 to 2.0
        atr_multiplier_sl=1.5,  # Tightened from 2.0 to 1.5
        atr_multiplier_tp=3.0  # Keep at 3.0 for better risk/reward (1:2 ratio)
    ):
        self.risk_percent = risk_percent
        self.atr_multiplier_sl = atr_multiplier_sl
        self.atr_multiplier_tp = atr_multiplier_tp

    def calculate_risk_amount(self, balance):
        """
        Amount of money to risk per trade.
        """
        return balance * (self.risk_percent / 100)

    def calculate_stop_loss(
        self,
        entry_price,
        atr=None,
        stop_loss_percent=2
    ):
        """
        Calculate Stop Loss.

        If ATR is available:
            Stop Loss = Entry - (ATR × Multiplier)

        Otherwise:
            Use fixed percentage.
        """

        if atr is not None and atr > 0:
            return entry_price - (atr * self.atr_multiplier_sl)

        return entry_price * (1 - stop_loss_percent / 100)

    def calculate_take_profit(
        self,
        entry_price,
        atr=None,
        take_profit_percent=4
    ):
        """
        Calculate Take Profit.

        If ATR is available:
            Take Profit = Entry + (ATR × Multiplier)

        Otherwise:
            Use fixed percentage.
        """

        if atr is not None and atr > 0:
            return entry_price + (atr * self.atr_multiplier_tp)

        return entry_price * (1 + take_profit_percent / 100)
