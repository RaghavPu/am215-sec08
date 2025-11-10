import time

def task_one():
    """Simulates a task that takes 1 second to complete."""
    print("Starting task one...")
    time.sleep(1)  # Simulate work
    print("Task one finished.")

def task_two():
    """Simulates another task that takes 1 second to complete."""
    print("Starting task two...")
    time.sleep(1)  # Simulate work
    print("Task two finished.")

def main():
    """Runs two tasks sequentially."""
    t0 = time.perf_counter()
    task_one()
    task_two()
    t1 = time.perf_counter()
    print(f"Total time: {t1 - t0:.2f} seconds")

if __name__ == "__main__":
    main()
