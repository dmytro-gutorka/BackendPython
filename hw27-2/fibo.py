from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 0:
        raise ValueError("Nubmer cannot be negative")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    n = 10
    print(f"Fibonacci({n}) =", fibonacci(n))
