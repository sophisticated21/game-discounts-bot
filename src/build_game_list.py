import requests
import json
import re
import time
from fetcher_review_count import ReviewFetcher

SEARCH_URL = ("https://store.steampowered.com/search/results/"
              "?query&specials=1&start=0&count=500&cc=br&l=en&infinite=1")

MIN_REVIEWS = 10000
OUTPUT_FILE = "data/games.json"

class GameListBuilder:
    def __init__(self):
        self.review_fetcher = ReviewFetcher()

    def fetch_discount_ids(self):
        try:
            r = requests.get(SEARCH_URL, timeout=10)
            data = r.json()

            html = data.get("results_html", "")
            if not html:
                print("[error] no results_html returned")
                return []

            # HTML içinden app_id çıkar
            app_ids = re.findall(r'data-ds-appid="(\d+)"', html)
            app_ids = list(set(app_ids))  # tekrarları sil

            print(f"Found {len(app_ids)} discounted ids.")
            return app_ids

        except Exception as e:
            print(f"[fetch error] {e}")
            return []

    def build_list(self):
        ids = self.fetch_discount_ids()
        result = []

        for app_id in ids:
            reviews = self.review_fetcher.get_review_count(app_id)

            if reviews is None:
                continue

            print(f"{app_id}: {reviews} reviews")

            if reviews >= MIN_REVIEWS:
                result.append(app_id)

            # Steam'e yüklenmeyelim
            time.sleep(0.5)

        return result

    def save_to_file(self, game_list):
        data = {"steam": game_list}

        try:
            with open(OUTPUT_FILE, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Saved {len(game_list)} games to {OUTPUT_FILE}")
        except Exception as e:
            print(f"[error] cannot save file: {e}")


if __name__ == "__main__":
    builder = GameListBuilder()
    games = builder.build_list()
    builder.save_to_file(games)