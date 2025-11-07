import asyncio
import time
import aiohttp

# A list of URLs to fetch. Using real but fast-responding sites.
URLS = ["https://www.google.com", "https://www.github.com", "https://www.python.org"] * 10

async def fetch(session: aiohttp.ClientSession, url: str) -> int:
    """
    Asynchronously fetches a URL using aiohttp and returns its content length.
    `session.get()` is an awaitable, so it yields control to the event loop.
    """
    async with session.get(url) as response:
        content = await response.read()
        return len(content)

async def main():
    """
    Fetches a list of URLs concurrently using asyncio and aiohttp.
    """
    print(f"Fetching {len(URLS)} URLs concurrently with asyncio...")
    t0 = time.perf_counter()

    # Create a single aiohttp session to be reused for all requests.
    async with aiohttp.ClientSession() as session:
        # Create a list of coroutines to run.
        tasks = [fetch(session, url) for url in URLS]
        # Run all tasks concurrently and gather their results.
        results = await asyncio.gather(*tasks)

    t1 = time.perf_counter()

    total_bytes = sum(results)
    print(f"Total bytes downloaded: {total_bytes:,}")
    print(f"Asyncio time: {t1 - t0:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())
