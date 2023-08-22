def kmp(a: str, b: str):
    '''
    a: string
    b: pattern
    '''
    # raise NotImplementedError("KMP not implemented")
    len_p = len(b)
    next_array = [0]
    # i, j = 0, 0
    # P = [0, 0, 1, 2, 3, 0, 0]
    ret = []
    temp = 1
    now = 0
    while temp < len_p:
        if b[now] == b[temp]:
            now += 1
            temp += 1
            next_array.append(now)
        elif now == 0:
            next_array.append(0)
            temp += 1
        else:
            now = next_array[now-1]

    i, j = 0, 0
    while i < len(a) and j < len_p:
        if a[i] == b[j]: i, j = i + 1, j + 1
        else:
            if j == 0: i += 1
            else: j = next_array[j - 1]
        if j == len(b):
            ret.append(i - j)
            j = next_array[j-1]
    return ret

def func(x: str):
    dp = [0] * len(x)
    for i in range(1, len(x)):
        ...

if __name__ == "__main__":
    '''
    Just for test.
    '''
    A = "abababaababacbababacb"
    B = "ababacb"

    print(kmp(A, B))