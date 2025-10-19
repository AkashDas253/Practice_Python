def binary_search(arr, target, verbose=False, issorted=True):

    """
    Return index of target in arr if found, else -1.
    If issorted is False, sorts a copy of arr before searching.
    """
    def _binary_search(a, target, verbose):
        left, right = 0, len(a) - 1
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
        # Find the index of the value in the original array
        try:
            return arr.index(sorted_arr[idx])
        except ValueError:
            return -1

    if not issorted:
        sorted_arr = sorted(arr)
        if verbose:
            print(f"[binary_search] Sorted array: {sorted_arr}")
        idx = _binary_search(sorted_arr, target, verbose)
        return find_index_in_original(arr, sorted_arr, idx)
    else:
        return _binary_search(arr, target, verbose)
