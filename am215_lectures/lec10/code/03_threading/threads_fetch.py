import time
import requests
from concurrent.futures import ThreadPoolExecutor

# A list of URLs to fetch. Using real but fast-responding sites.
URLS = ["https://www.google.com", "https://www.github.com", "https://www.python.org"] * 10

def fetch(url):
    """Fetches a URL and returns the number of bytes read."""
    r = requests.get(url, timeout=10)
    return len(r.content)

def main():
    """Fetches a list of URLs concurrently using threads."""
    print(f"Fetching {len(URLS)} URLs concurrently with threads...")
    t0 = time.perf_counter()
    # Using max_workers=20 to allow many I/O operations to be "in flight".
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(fetch, URLS))
    t1 = time.perf_counter()

    total_bytes = sum(results)
    print(f"Total bytes downloaded: {total_bytes:,}")
    print(f"Threading time: {t1 - t0:.3f}s")

if __name__ == "__main__":
    main()
