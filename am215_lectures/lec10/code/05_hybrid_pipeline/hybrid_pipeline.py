import asyncio
import sys
import time

import aiohttp
import numpy as np
from aiohttp import web

# --- CPU-Bound Analysis Function (to be run in a thread) ---


def analyze_data(data: bytes, sample_rate: int) -> tuple[float, float]:
    """
    Performs a CPU-intensive analysis on raw byte data.

    This function is designed to be synchronous and blocking. It simulates a
    real-world scientific task that involves numerical computation. NumPy
    releases the GIL for many operations, so this can run in parallel with
    other threads.

    Parameters
    ----------
    data : bytes
        The raw byte string representing a 1D float64 signal.
    sample_rate : int
        The sample rate of the signal, used for frequency analysis.

    Returns
    -------
    tuple[float, float]
        A tuple containing the mean of the signal and its dominant frequency.
    """
    # 1. Convert bytes to a NumPy array
    signal = np.frombuffer(data, dtype=np.float64)

    # 2. Perform a computationally intensive task (FFT)
    fft_result = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(len(signal), d=1 / sample_rate)

    # 3. Find the dominant frequency
    # We only look at the positive frequencies
    positive_freq_indices = np.where(fft_freq > 0)
    dominant_freq_index = positive_freq_indices[0][
        np.argmax(np.abs(fft_result[positive_freq_indices]))
    ]
    dominant_frequency = fft_freq[dominant_freq_index]

    # 4. Calculate a simple statistic
    mean_val = np.mean(signal)

    return mean_val, dominant_frequency


# --- Async I/O and Orchestration ---


async def fetch_and_process(
    session: aiohttp.ClientSession, url: str, sample_rate: int
) -> tuple[str, float, float]:
    """
    Fetches data from a URL and offloads its analysis to a thread.

    Parameters
    ----------
    session : aiohttp.ClientSession
        The client session for making HTTP requests.
    url : str
        The URL to fetch the data from.
    sample_rate : int
        The sample rate of the signal to be analyzed.

    Returns
    -------
    tuple[str, float, float]
        A tuple containing the URL, the calculated mean, and the dominant frequency.
    """
    print(f"Fetching {url}...")
    async with session.get(url) as response:
        if response.status != 200:
            print(f"Error fetching {url}: Status {response.status}")
            return url, -1.0, -1.0

        raw_data = await response.read()
        print(f"Analyzing {url} in a separate thread...")

        # Offload the blocking, CPU-bound `analyze_data` function to a
        # separate thread. `asyncio.to_thread` manages the thread pool
        # and returns an awaitable that completes when the function is done.
        mean_val, dominant_freq = await asyncio.to_thread(
            analyze_data, raw_data, sample_rate
        )

        print(f"Finished analysis for {url}")
        return url, mean_val, dominant_freq


async def main():
    """
    Main coroutine to set up a local server, run the hybrid pipeline,
    and print results.
    """
    # --- 1. Set up a local server to provide data ---
    async def handle_data_request(request: web.Request) -> web.Response:
        """Generates and serves random signal data as bytes."""
        n_samples = int(request.query.get("n_samples", "1000000"))
        # Generate a signal with a random dominant frequency
        sample_rate = 1000
        time_vec = np.arange(n_samples) / sample_rate
        freq = np.random.uniform(50, 150)
        signal = np.sin(2 * np.pi * freq * time_vec) + 0.5 * np.random.randn(n_samples)
        return web.Response(body=signal.astype(np.float64).tobytes())

    app = web.Application()
    app.router.add_get("/data", handle_data_request)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8080)
    await site.start()
    print("Local data server started at http://localhost:8080/data")

    # --- 2. Run the pipeline ---
    N_TASKS = 20
    SAMPLE_RATE = 1000
    URL = f"http://localhost:8080/data?n_samples={SAMPLE_RATE * 5}"
    urls = [URL] * N_TASKS

    print(f"\nStarting hybrid pipeline for {N_TASKS} tasks...")
    t0 = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_process(session, url, SAMPLE_RATE) for url in urls]
        results = await asyncio.gather(*tasks)

    t1 = time.perf_counter()

    # --- 3. Clean up and report results ---
    await runner.cleanup()
    print("Local data server stopped.")

    print("\n--- Analysis Results ---")
    for url, mean, freq in results:
        print(f"Source: {url.split('?')[0]} -> Mean: {mean:6.3f}, Freq: {freq:6.2f} Hz")

    print("\n--- Summary ---")
    print(f"Completed {N_TASKS} fetch-and-process tasks in {t1 - t0:.3f} seconds.")
    print(
        "Pattern: `asyncio` handled I/O, `threading` handled CPU-bound NumPy analysis."
    )


if __name__ == "__main__":
    # On Windows, the default event loop policy may cause issues with aiohttp.
    # ProactorEventLoop is recommended for server/client applications.
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            # This can happen on graceful shutdown in some environments.
            pass
        else:
            raise
