def fibonacci(n):
    lst = [None for _ in range(n+1)]

    for i in range(n+1):
        if i == 0 or i == 1:
            lst[i] = i
        else:
            lst[i] = lst[i-1] + lst[i-2]

    return lst[n]


print(fibonacci(35))
