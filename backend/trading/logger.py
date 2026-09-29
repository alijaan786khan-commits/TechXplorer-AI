import csv
import os


class TradeLogger:

    FILE_NAME = "backend/trading/logs/trades.csv"

    @staticmethod
    def log(action, price, balance, profit=0):

        os.makedirs("backend/trading/logs", exist_ok=True)

        file_exists = os.path.isfile(TradeLogger.FILE_NAME)

        with open(TradeLogger.FILE_NAME, "a", newline="") as file:

            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Time",
                    "Action",
                    "Price",
                    "Profit",
                    "Balance"
                ])

            from datetime import datetime
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                action,
                round(price, 2),
                round(profit, 2),
                round(balance, 2)
            ])
