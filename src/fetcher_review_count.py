import requests

class ReviewFetcher:
    def __init__(self):
        pass

    def get_review_count(self, app_id):
        url = (
            f"https://store.steampowered.com/appreviews/"
            f"{app_id}?json=1&language=all&purchase_type=all"
        )

        try:
            r = requests.get(url, timeout=10)
            data = r.json()

            summary = data.get("query_summary")
            if not summary:
                print(f"[review error] no summary for {app_id}")
                return None

            total = summary.get("total_reviews")
            if total is None:
                print(f"[review error] no review count for {app_id}")
                return None

            return total

        except Exception as e:
            print(f"[review fetch error] {app_id}: {e}")
            return None