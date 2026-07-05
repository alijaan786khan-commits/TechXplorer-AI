import json
import os


class StateManager:

    FILE_NAME = "backend/trading/state.json"

    @staticmethod
    def load_state():

        if not os.path.exists(StateManager.FILE_NAME):

            return {
                "balance": 100.0,
                "position": None,
                "entry_price": 0,
                "stop_loss": 0,
                "take_profit": 0
            }

        with open(StateManager.FILE_NAME, "r") as file:
            return json.load(file)

    @staticmethod
    def save_state(balance, position, entry_price, stop_loss, take_profit):

        data = {
            "balance": balance,
            "position": position,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit
        }

        with open(StateManager.FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)