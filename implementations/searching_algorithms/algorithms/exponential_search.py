def exponential_search(arr, target, verbose=False, issorted=True):

    """
    Exponential Search algorithm. If issorted is False, sorts a copy of arr before searching.
    Returns index in original array if found, else -1.
    """
    def _exponential_search(a, target, verbose):
        if len(a) == 0:
            return -1
        if a[0] == target:
            if verbose:
                print(f"Found at index 0")
            return 0
        i = 1
        while i < len(a) and a[i] <= target:
            if verbose:
                print(f"Exponentially increasing i: {i}")
            i *= 2
        left = i // 2
        right = min(i, len(a)-1)
        if verbose:
            print(f"Binary search between {left} and {right}")
        while left <= right:
            mid = (left + right) // 2
            if verbose:
                print(f"Checking index {mid}: {a[mid]}")
            if a[mid] == target:
                return mid
            elif a[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def find_index_in_original(arr, sorted_arr, idx):
        if idx == -1:
            return -1
        try:
            return arr.index(sorted_arr[idx])
        except ValueError:
            return -1

    if not issorted:
        sorted_arr = sorted(arr)
        if verbose:
            print(f"[exponential_search] Sorted array: {sorted_arr}")
        idx = _exponential_search(sorted_arr, target, verbose)
        return find_index_in_original(arr, sorted_arr, idx)
    else:
        return _exponential_search(arr, target, verbose)
