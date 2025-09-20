def binary_search(arr, target, verbose=False):
    """Return index of target in arr if found, else -1. Assumes arr is sorted."""
    left, right = 0, len(arr) - 1
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
