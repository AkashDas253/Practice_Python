def linear_search(arr, target, verbose=False):
    """Return index of target in arr if found, else -1."""
    for i, value in enumerate(arr):
        if verbose:
            print(f"Checking index {i}: {value}")
        if value == target:
            return i
    return -1
