import threading

# A shared variable
counter = 0

def increment():
    """
    Increments the global counter. This function is not thread-safe.
    The operation `counter += 1` is not atomic.
    """
    global counter
    # This operation involves three steps: read, increment, write.
    # A thread can be interrupted between these steps, leading to lost updates.
    counter += 1

def main():
    """
    Demonstrates a race condition by having multiple threads increment a
    shared counter without a lock.
    """
    NUM_THREADS = 100_000
    print(f"Attempting to increment a counter {NUM_THREADS:,} times with threads...")

    threads = [threading.Thread(target=increment) for _ in range(NUM_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Final counter value: {counter}")
    print(f"Expected value: {NUM_THREADS}")
    if counter != NUM_THREADS:
        print("Race condition occurred: The final value is incorrect!")

if __name__ == "__main__":
    main()
