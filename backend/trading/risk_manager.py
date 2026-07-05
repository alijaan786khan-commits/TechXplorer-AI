class RiskManager:

    def __init__(self, risk_percent=1.0):
        self.risk_percent = risk_percent

    def calculate_risk_amount(self, balance):
        """
        Calculate how much money we are willing to risk.
        Example:
        Balance = $100
        Risk = 1%
        Risk Amount = $1
        """
        return balance * (self.risk_percent / 100)

    def calculate_stop_loss(self, entry_price, stop_loss_percent=2):
        """
        Calculate Stop Loss price.
        Example:
        Entry = 60000
        Stop Loss = 2%
        Result = 58800
        """
        return entry_price * (1 - stop_loss_percent / 100)

    def calculate_take_profit(self, entry_price, take_profit_percent=4):
        """
        Calculate Take Profit price.
        Example:
        Entry = 60000
        Take Profit = 4%
        Result = 62400
        """
        return entry_price * (1 + take_profit_percent / 100)