import json
from fetcher import PriceFetcher
from fetcher_review_count import ReviewFetcher
from scoring import score_game
from posted_manager import PostedManager
from tweet_format import format_tweet


def load_game_ids():
    try:
        with open("data/games.json", "r") as f:
            data = json.load(f)
            return data.get("steam", [])
    except:
        return []


def run():
    fetcher = PriceFetcher()
    review_fetcher = ReviewFetcher()
    posted = PostedManager()

    game_list = load_game_ids()
    print(f"Loaded {len(game_list)} games.")

    candidates = []

    for app_id in game_list:
        price_info = fetcher.get_steam_price(app_id)
        if price_info is None:
            continue

        name = price_info["name"]
        discount = price_info["discount_percent"]
        final_price = price_info["final"]
        currency = price_info["currency"]
        original = price_info["original"]

        # review count
        review_count = review_fetcher.get_review_count(app_id)
        if review_count is None:
            continue

        # no discount → skip
        if discount == 0:
            continue

        # spam engeli
        if not posted.should_post(app_id, discount, final_price):
            continue

        # puan
        score = score_game(review_count, discount)

        candidates.append({
            "app_id": app_id,
            "name": name,
            "discount": discount,
            "price": final_price,
            "original": original,
            "currency": currency,
            "review": review_count,
            "score": score
        })

    # puana göre sırala
    candidates.sort(key=lambda x: x["score"], reverse=True)

    # günlük en fazla 10 oyun
    selected = candidates[:10]

    print("\n=== Today’s Picks ===\n")

    for item in selected:
        print(f"{item['name']} — {item['discount']}% off — {item['price']} {item['currency']}")
        posted.update(item["app_id"], item["discount"], item["price"])
        tweet = format_tweet(item)
        print(tweet)
        print("---------------------------")

if __name__ == "__main__":
    run()