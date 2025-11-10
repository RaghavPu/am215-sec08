# 04: Asyncio Examples

This directory introduces `asyncio` for highly scalable, single-threaded concurrency for I/O-bound tasks.

-   `async_fanout.py`: Demonstrates how `asyncio.gather` can run many non-blocking `asyncio.sleep` tasks concurrently, showing how the event loop overlaps waits without the overhead of multiple threads.
-   `async_fetch.py`: The URL fetching task implemented using `asyncio` and an `async`-compatible HTTP library (`aiohttp`). This demonstrates the modern approach to massive I/O concurrency. Note that this requires installing dependencies as described in the main `README.md` for this lecture's code.
