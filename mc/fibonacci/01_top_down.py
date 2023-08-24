def fibonacci(n, cache):
    if n not in cache:
        if n == 0 or n == 1:
            cache[n] = n
        else:
            cache[n] = fibonacci(n-1, cache) + fibonacci(n-2, cache)

    return cache[n]

print(fibonacci(1440, {}))
