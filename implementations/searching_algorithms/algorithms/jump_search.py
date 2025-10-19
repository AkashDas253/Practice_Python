import math

def jump_search(arr, target, verbose=False, issorted=True):

    """
    Jump Search algorithm. If issorted is False, sorts a copy of arr before searching.
    Returns index in original array if found, else -1.
    """
    def _jump_search(a, target, verbose):
        n = len(a)
        step = int(math.sqrt(n))
        prev = 0
        if verbose:
            print(f"Jump step: {step}")
        while prev < n and a[min(step, n)-1] < target:
            if verbose:
                print(f"Jumping from {prev} to {min(step, n)-1}")
            prev = step
            step += int(math.sqrt(n))
            if prev >= n:
                return -1
        for i in range(prev, min(step, n)):
            if verbose:
                print(f"Checking index {i}: {a[i]}")
            if a[i] == target:
                return i
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
            print(f"[jump_search] Sorted array: {sorted_arr}")
        idx = _jump_search(sorted_arr, target, verbose)
        return find_index_in_original(arr, sorted_arr, idx)
    else:
        return _jump_search(arr, target, verbose)
