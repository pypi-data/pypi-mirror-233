from __init__ import *

def min(x, y):
    return x if x < y else y

def max(x, y):
    return x if x > y else y

def abs(x):
    if x < 0:
        return -x
    return x

def pow(x, y, mod = 998244353):
    res = 1
    while y:
        if y & 1:    
            res = res * x % mod 
        x *= x   
        y >>= 1
    return res

def sqrt(x, prec = 1e-6):
    if x < 0:
        pass
    y = x
    while abs(x - pow(y, 2)) > prec:
        y = (y + x / y) / 2
    return y

def fac(x):
    return 1 if not x or x == 1 else x * fac(x)

def a(n, m):
    return fac(n) / fac(n - m)

def c(n, m):
    m = min(m, n - m)
    return a(n, m) / a(m, m)

def fib(n):
    if n < 2:
        return n
    x, y = fib((n >> 1) - 1), fib(n >> 1)
    if n & 0x1:
        x += y
        return x * x + y * y
    else:
        return y * (y + 2 * x)
    
def ispri(x):
    if x == 1:
        return False
    for i in range(2, int(sqrt(x)) + 1):
        if not x % i:
            return False
    return True

def lsieve(n):
    cnt, st, pri = 0, [False] * (n << 1), [0] * (n << 1)
    for i in range(2, n + 1):
        if not st[i]:
            pri[cnt] = i
            cnt += 1
        for j in range(cnt):
            if pri[j] * i > n: 
                break
            st[pri[j] * i] = True
            if not i % pri[j]: 
                break
    return st

def factor(x):
    st = lsieve(x)
    faclst = []
    for i in range(2, int(sqrt(x)) + 1):
        if st[i]:
            continue
        cnt = 0
        while not x % i:
            cnt += 1
            x /= i
        if cnt:
            faclst.append([i, cnt])
    if x > 1:
        faclst.append([x, 1])
    return faclst