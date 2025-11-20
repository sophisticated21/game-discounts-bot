import requests

class EpicFreeFetcher:
    def __init__(self, country="BR", locale="pt-BR"):
        self.country = country
        self.locale = locale
        self.url = (
            "https://store-site-backend-static.ak.epicgames.com/"
            f"freeGamesPromotions?locale={locale}&country={country}&allowCountries={country}"
        )

    def get_free_games(self):
        try:
            r = requests.get(self.url, timeout=10)
            data = r.json()
        except Exception as e:
            print("Epic fetch error:", e)
            return []

        games = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])
        free_list = []

        for g in games:
            title = g.get("title")
            product_slug = g.get("productSlug") or ""
            offer = g.get("promotions")

            if not offer:
                continue

            promo = offer.get("promotionalOffers") or []
            upcoming = offer.get("upcomingPromotionalOffers") or []

            # current free offer
            if promo:
                p = promo[0]["promotionalOffers"][0]
                start = p["startDate"]
                end = p["endDate"]

                free_list.append({
                    "title": title,
                    "slug": product_slug,
                    "start": start,
                    "end": end
                })

        return free_list