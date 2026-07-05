from logger import TradeLogger
from state_manager import StateManager


class PaperTrader:

    def __init__(self):

        state = StateManager.load_state()

        self.balance = state["balance"]
        self.position = state["position"]
        self.entry_price = state["entry_price"]
        self.stop_loss = state.get("stop_loss", 0)
        self.take_profit = state.get("take_profit", 0)

        # Fixed paper trading size
        self.trade_size = 100

    def save(self):

        StateManager.save_state(
            self.balance,
            self.position,
            self.entry_price,
            self.stop_loss,
            self.take_profit
        )

    def buy(self, price, stop_loss, take_profit):

        if self.position is not None:
            return

        self.position = "LONG"
        self.entry_price = price
        self.stop_loss = stop_loss
        self.take_profit = take_profit

        TradeLogger.log("BUY", price, self.balance)

        self.save()

        print("\n✅ PAPER BUY")
        print(f"Entry Price : {price:.2f}")
        print(f"Stop Loss   : {stop_loss:.2f}")
        print(f"Take Profit : {take_profit:.2f}")

    def sell(self, price):

        if self.position != "LONG":
            return

        # Percentage movement
        change_percent = (price - self.entry_price) / self.entry_price

        # Profit based on trade size
        profit = change_percent * self.trade_size

        self.balance += profit

        TradeLogger.log("SELL", price, self.balance)

        print("\n✅ PAPER SELL")
        print(f"Exit Price  : {price:.2f}")
        print(f"Profit/Loss : {profit:.2f} USDT")
        print(f"Balance     : {self.balance:.2f} USDT")

        self.position = None
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0

        self.save()

    def check_exit(self, current_price):

        if self.position != "LONG":
            return

        if current_price <= self.stop_loss:

            print("\n🛑 STOP LOSS HIT")
            self.sell(current_price)

        elif current_price >= self.take_profit:

            print("\n🎯 TAKE PROFIT HIT")
            self.sell(current_price)