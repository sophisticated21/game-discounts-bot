import json
from fetcher import PriceFetcher
from checker import PriceChecker

def load_game_ids():
    try:
        with open("data/games.json", "r") as f:
            data = json.load(f)
            return data.get("steam", [])
    except Exception as e:
        print(f"[load error] {e}")
        return []

def run():
    fetcher = PriceFetcher()
    checker = PriceChecker()

    game_list = load_game_ids()
    print(f"Loaded {len(game_list)} games.")

    for app_id in game_list:
        info = fetcher.get_steam_price(app_id)

        if info is None:
            print(f"[warning] no data for {app_id}")
            continue

        name = info["name"]
        new_price = info["final"]
        original_price = info["original"]
        percent = info["discount_percent"]
        currency = info["currency"]

        change = checker.check_discount(app_id, new_price)

        if percent > 0:
            print(f"{name} is {percent}% off: {original_price} → {new_price} {currency}")
        else:
            print(f"{name} has no discount.")

    checker.save()

if __name__ == "__main__":
    run()