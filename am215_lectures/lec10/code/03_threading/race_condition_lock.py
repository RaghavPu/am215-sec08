import threading

# A shared variable and a lock to protect it
counter = 0
lock = threading.Lock()

def increment():
    """
    Increments the global counter safely using a lock to prevent race conditions.
    """
    global counter
    # The 'with' statement automatically acquires and releases the lock.
    # This ensures that only one thread can execute the code inside this
    # block at a time, making the increment operation atomic.
    with lock:
        counter += 1

def main():
    """
    Demonstrates the use of a lock to prevent a race condition, ensuring
    the shared counter is incremented correctly.
    """
    NUM_THREADS = 100_000
    print(f"Incrementing a counter {NUM_THREADS:,} times with a lock...")

    threads = [threading.Thread(target=increment) for _ in range(NUM_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Final counter value: {counter}")
    print(f"Expected value: {NUM_THREADS}")
    if counter == NUM_THREADS:
        print("Success: The lock prevented the race condition.")

if __name__ == "__main__":
    main()
