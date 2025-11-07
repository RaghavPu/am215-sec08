import time
import requests

# A list of URLs to fetch. Using real but fast-responding sites.
URLS = ["https://www.google.com", "https://www.github.com", "https://www.python.org"] * 10

def fetch(url):
    """Fetches a URL and returns the number of bytes read."""
    r = requests.get(url, timeout=10)
    return len(r.content)

def main():
    """Fetches a list of URLs sequentially."""
    print(f"Fetching {len(URLS)} URLs sequentially...")
    t0 = time.perf_counter()
    results = [fetch(u) for u in URLS]
    t1 = time.perf_counter()

    total_bytes = sum(results)
    print(f"Total bytes downloaded: {total_bytes:,}")
    print(f"Sequential time: {t1 - t0:.3f}s")

if __name__ == "__main__":
    main()
