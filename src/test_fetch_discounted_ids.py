import requests
import re

def fetch_discount_ids():
    url = ("https://store.steampowered.com/search/results/"
           "?query&specials=1&start=0&count=500&cc=br&l=en&infinite=1")

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        html = data.get("results_html", "")
        if not html:
            print("[error] no html returned")
            return []

        # HTML içinden app id'leri çıkar
        app_ids = re.findall(r'data-ds-appid="(\d+)"', html)
        return list(set(app_ids))  # tekrar edenleri temizle

    except Exception as e:
        print(f"[fetch error] {e}")
        return []


if __name__ == "__main__":
    ids = fetch_discount_ids()
    print(f"Found {len(ids)} ids:")
    print(ids[:30])  # ilk 30 tanesini göster