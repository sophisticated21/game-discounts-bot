import requests
import time

class PriceFetcher:
    def __init__(self):
        pass

    def get_steam_price(self, app_id):
        url = (
            f"https://store.steampowered.com/api/appdetails"
            f"?appids={app_id}&cc=br&l=en&filters=basic,price_overview"
        )

        try:
            r = requests.get(url, timeout=10)
            data = r.json()

            block = data.get(str(app_id))
            if not block or block.get("success") is not True:
                print(f"[steam error] fetch failed for {app_id}")
                return None

            game = block.get("data", {})
            name = game.get("name")
            price = game.get("price_overview")

            if not name:
                print(f"[steam warning] name missing for {app_id}")
                return None

            if not price:
                print(f"[steam warning] price info missing for {app_id}")
                return None

            # Son tarih kontrolü
            end_ts = price.get("discount_expiration")
            if end_ts:
                end_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_ts))
            else:
                end_date = None

            return {
                "app_id": app_id,
                "name": name,
                "original": price["initial"] / 100,
                "final": price["final"] / 100,
                "discount_percent": price["discount_percent"],
                "currency": price["currency"],
                "discount_end": end_date
            }

        except Exception as e:
            print(f"[steam fetch error] {app_id}: {e}")
            return None