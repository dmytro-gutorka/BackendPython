import redis


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def fibonacci(n):
    if n < 0:
        raise ValueError("Number cannot be negative")

    cached_value = redis_client.get(f"fibonacci:{n}")
    if cached_value:
        return int(cached_value)

    if n == 0:
        return 0
    elif n == 1:
        return 1

    fib_value = fibonacci(n - 1) + fibonacci(n - 2)

    redis_client.set(f"fibonacci:{n}", fib_value)

    return fib_value


if __name__ == "__main__":
    n = 100
    print(f"Fibonacci({n}) = {fibonacci(n)}")
