def mergesort(arr, verbose=False):
    def _mergesort(arr, depth=1):
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]
            if verbose:
                print(f"{'  '*depth}Splitting: {arr}")
            _mergesort(L, depth+1)
            _mergesort(R, depth+1)
            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
            if verbose:
                print(f"{'  '*depth}Merged: {arr}")
    _mergesort(arr)
    if verbose:
        print(f"Final sorted array: {arr}")
