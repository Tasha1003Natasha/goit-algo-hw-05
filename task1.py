def caching_fibonacci():
    # функції caching_fibonacci, яка обчислює числа Фібоначчі з використанням кешування:
    cache = {}

    def fibonacci(n):
        if not isinstance(n, int) or n < 0:
            print("Error: please enter a non-negative integer.")
            return None

        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


fib = caching_fibonacci()
print(fib(10))
print(fib(15))
