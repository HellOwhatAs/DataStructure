def KMP(a: str, b: str):
    i, j = 0, 0
    P = [0, 0, 1, 2, 3, 0, 0]
    ret = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]: i, j = i + 1, j + 1
        else:
            if j == 0: i += 1
            else: j = P[j - 1]
        if j == len(b):
            ret.append(i - j)
            j = 0
    return ret

def func(x: str):
    dp = [0] * len(x)
    for i in range(1, len(x)):
        ...

A = "abababaababacbababacb"
B = "ababacb"

print(KMP(A, B))