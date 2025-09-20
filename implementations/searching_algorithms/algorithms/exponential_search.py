def exponential_search(arr, target, verbose=False):
    if len(arr) == 0:
        return -1
    if arr[0] == target:
        if verbose:
            print(f"Found at index 0")
        return 0
    i = 1
    while i < len(arr) and arr[i] <= target:
        if verbose:
            print(f"Exponentially increasing i: {i}")
        i *= 2
    left = i // 2
    right = min(i, len(arr)-1)
    if verbose:
        print(f"Binary search between {left} and {right}")
    while left <= right:
        mid = (left + right) // 2
        if verbose:
            print(f"Checking index {mid}: {arr[mid]}")
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
