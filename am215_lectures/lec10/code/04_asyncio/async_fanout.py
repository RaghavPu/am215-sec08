import asyncio
import time

async def ioish(task_id: int):
    """
    A coroutine that simulates a non-blocking I/O operation.
    `asyncio.sleep` yields control back to the event loop.
    """
    print(f"Task {task_id}: Starting I/O wait.")
    await asyncio.sleep(0.1)  # Simulate a non-blocking 100ms I/O wait
    print(f"Task {task_id}: Finished I/O wait.")
    return task_id

async def main(n_tasks: int = 30):
    """
    Runs many `ioish` coroutines concurrently using `asyncio.gather`.
    """
    print(f"Running {n_tasks} asyncio tasks concurrently...")
    t0 = time.perf_counter()
    # asyncio.gather runs all awaitables in the sequence concurrently.
    # The `*` unpacks the generator into arguments for gather.
    results = await asyncio.gather(*(ioish(i) for i in range(n_tasks)))
    t1 = time.perf_counter()

    print(f"Results: {results}")
    print(f"Asyncio with {n_tasks} tasks finished in {t1 - t0:.3f}s")
    print("Note: Total time is ~0.1s, not 3.0s, because all waits were overlapped.")

if __name__ == "__main__":
    # asyncio.run() starts the event loop and runs the main coroutine.
    asyncio.run(main())
