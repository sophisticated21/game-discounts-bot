import json
import os
from datetime import datetime, timedelta

POSTED_FILE = "data/posted.json"
DATE_FORMAT = "%Y-%m-%d"

class PostedManager:
    def __init__(self):
        self.data = self.load()

    def load(self):
        if not os.path.exists(POSTED_FILE):
            return {}
        try:
            with open(POSTED_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    def save(self):
        with open(POSTED_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def should_post(self, app_id, new_percent, new_price):
        """
        Returns True if:
        - game has never been posted
        - or discount increased compared to last time
        - or last post was more than 7 days ago
        """
        today = datetime.today().strftime(DATE_FORMAT)

        # Case 1: First time posting this game
        if app_id not in self.data:
            return True

        record = self.data[app_id]
        last_date = datetime.strptime(record["last_post_date"], DATE_FORMAT)
        last_percent = record["last_percent"]
        last_price = record["last_price"]

        # Case 2: Discount increased → always post
        if new_percent > last_percent:
            return True

        # Case 3: 7 days rule
        if datetime.today() - last_date >= timedelta(days=7):
            return True

        # Otherwise skip
        return False

    def update(self, app_id, new_percent, new_price):
        today = datetime.today().strftime(DATE_FORMAT)

        self.data[app_id] = {
            "last_post_date": today,
            "last_percent": new_percent,
            "last_price": new_price
        }
        self.save()