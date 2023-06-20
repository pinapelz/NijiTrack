import time


def log(message: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("TASK: " + message)
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"COMPLETE: {message} {round(end - start, 3)} seconds")
            return result

        return wrapper

    return decorator
