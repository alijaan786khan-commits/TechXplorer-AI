import pandas as pd


class Backtester:

    def __init__(self, starting_balance=100):
        self.balance = starting_balance
        self.position = None
        self.entry_price = 0

        self.total_trades = 0
        self.wins = 0
        self.losses = 0

        self.total_profit = 0

    def buy(self, price):

        if self.position is not None:
            return

        self.position = "LONG"
        self.entry_price = price

    def sell(self, price):

        if self.position != "LONG":
            return

        profit_percent = (
            (price - self.entry_price)
            / self.entry_price
        )

        profit = self.balance * profit_percent

        self.balance += profit
        self.total_profit += profit
        self.total_trades += 1

        if profit > 0:
            self.wins += 1
        else:
            self.losses += 1

        self.position = None
        self.entry_price = 0

    def report(self):

        print("\n")
        print("=" * 60)
        print("TECHXPLORER AI BACKTEST REPORT")
        print("=" * 60)

        print(f"Balance      : ${self.balance:.2f}")
        print(f"Trades       : {self.total_trades}")
        print(f"Wins         : {self.wins}")
        print(f"Losses       : {self.losses}")

        if self.total_trades > 0:
            win_rate = (
                self.wins /
                self.total_trades
            ) * 100
        else:
            win_rate = 0

        print(f"Win Rate     : {win_rate:.2f}%")
        print(f"Profit       : ${self.total_profit:.2f}")

        print("=" * 60)