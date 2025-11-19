import json
import os

class PriceChecker:
    def __init__(self, log_path="data/prices.json"):
        self.log_path = log_path
        self.data = self._load_data()

    def _load_data(self):
        try:
            if not os.path.exists(self.log_path):
                return {}
            with open(self.log_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[load error] {e}")
            return {}

    def save(self):
        try:
            with open(self.log_path, "w") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"[save error] {e}")

    def check_discount(self, key, new_price):
        if new_price is None:
            print(f"[check warning] new price missing for {key}")
            return None

        old_price = self.data.get(key)

        if old_price is None:
            self.data[key] = new_price
            return None

        if new_price < old_price:
            drop = old_price - new_price
            self.data[key] = new_price
            return drop

        self.data[key] = new_price
        return None