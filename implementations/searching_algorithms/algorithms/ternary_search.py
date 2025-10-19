def ternary_search(arr, target, verbose=False, issorted=True):
    """
    Ternary Search algorithm. If issorted is False, sorts a copy of arr before searching.
    Returns index in original array if found, else -1.
    """
    def _ternary_search(a, left, right, target, verbose):
        while left <= right:
            third = (right - left) // 3
            mid1 = left + third
            mid2 = right - third
            if verbose:
                print(f"Checking indices {mid1}: {a[mid1]}, {mid2}: {a[mid2]}")
            if a[mid1] == target:
                return mid1
            if a[mid2] == target:
                return mid2
            if target < a[mid1]:
                right = mid1 - 1
            elif target > a[mid2]:
                left = mid2 + 1
            else:
                left = mid1 + 1
                right = mid2 - 1
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
            print(f"[ternary_search] Sorted array: {sorted_arr}")
        idx = _ternary_search(sorted_arr, 0, len(sorted_arr)-1, target, verbose)
        return find_index_in_original(arr, sorted_arr, idx)
    else:
        return _ternary_search(arr, 0, len(arr)-1, target, verbose)
