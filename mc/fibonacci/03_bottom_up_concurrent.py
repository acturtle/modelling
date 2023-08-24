def fibonacci(n):
    count = 1
    a = 0
    b = 1

    while count < n:
        c = a + b
        a, b = b, c
        count += 1

    return c


print(fibonacci(35))
