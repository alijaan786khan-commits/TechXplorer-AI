import csv
import os


class Statistics:

    FILE_NAME = "backend/trading/logs/trades.csv"

    @staticmethod
    def get_stats():

        if not os.path.exists(Statistics.FILE_NAME):
            return {
                "total": 0,
                "wins": 0,
                "losses": 0,
                "profit": 0
            }

        total = 0
        wins = 0
        losses = 0
        profit = 0

        with open(Statistics.FILE_NAME, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                # Only completed SELL trades count
                if row["Action"] != "SELL":
                    continue

                total += 1

                p = float(row["Profit"])

                profit += p

                if p > 0:
                    wins += 1

                elif p < 0:
                    losses += 1

        return {
            "total": total,
            "wins": wins,
            "losses": losses,
            "profit": profit
        }