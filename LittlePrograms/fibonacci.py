import math

def fibonacci(n):
    fib_series = [0, 1]
    while fib_series[-1] < n:
        fib_series.append(fib_series[-1] + fib_series[-2])
    return fib_series

def harmonic_series(n):
    return sum(1.0/i for i in range(1, n+1))

def binomial_series(n, x):
    return sum((x**i)/math.factorial(i) for i in range(n+1))

def power_series(n, x):
    return sum(x**i for i in range(n+1))

def taylor_series(n, x, a=0):
    return sum((x-a)**i/math.factorial(i) for i in range(n+1))

print(fibonacci(100))
print(harmonic_series(10))
print(binomial_series(10, 2))
print(power_series(10, 2))
print(taylor_series(10, 2))