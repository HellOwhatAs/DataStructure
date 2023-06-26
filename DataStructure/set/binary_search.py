from typing import List, Any

def binary_search(ascending: List[Any], val: Any, start: int = 0, end: int = None):
    if end is None: end = len(ascending)
    if start == end: return start
    mid_idx = (start + end) // 2
    mid_val = ascending[mid_idx]
    if mid_val == val: return mid_idx
    if mid_val > val: return binary_search(ascending, val, start, mid_idx)
    return binary_search(ascending, val, mid_idx + 1, end)


if __name__ == '__main__':
    print(binary_search([i**2 for i in range(20)], 17))