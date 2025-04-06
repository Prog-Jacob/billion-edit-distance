import re
import csv
import time


def execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Running {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"Execution time: {time.time() - start_time:.4f} seconds")
        return result

    return wrapper


def save_csv(filename, data, fieldnames):
    """Saves a list of dictionaries to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def load_csv(filename):
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def process_title(title):
    title = title.lower()
    title = re.sub(r"[^a-z\s]", "", title)
    title = re.sub("\s+", " ", title)
    return title.strip()
