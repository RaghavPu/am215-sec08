import time
import functools

def time_it(func):
    """A decorator that prints the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """The wrapper function that adds timing behavior."""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"'{func.__name__}' took {end - start:.4f}s to execute.")
        return result
    return wrapper

@time_it
def do_work(duration):
    """A simple function that simulates work by sleeping."""
    print(f"Doing work for {duration}s...")
    time.sleep(duration)
    print("Work done.")
    return duration * 10

if __name__ == "__main__":
    print("--- Using the decorator with '@' syntax ---")
    result = do_work(0.5)
    print(f"Result: {result}\n")

    # --- The explicit, "under the hood" way ---
    print("--- Using the decorator with explicit assignment ---")
    
    def do_other_work(duration):
        """Another simple function that simulates work."""
        print(f"Doing other work for {duration}s...")
        time.sleep(duration)
        print("Other work done.")
        return duration * 20

    # Manually apply the decorator
    decorated_work = time_it(do_other_work)
    
    # Call the decorated version
    other_result = decorated_work(0.3)
    print(f"Result: {other_result}")
