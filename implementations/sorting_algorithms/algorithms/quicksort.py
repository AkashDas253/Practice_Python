def quicksort(arr, verbose=False):
    def _quicksort(arr, low, high, depth=1):
        if low < high:
            pi = partition(arr, low, high, depth)
            _quicksort(arr, low, pi-1, depth+1)
            _quicksort(arr, pi+1, high, depth+1)
    def partition(arr, low, high, depth):
        pivot = arr[high]
        i = low - 1
        if verbose:
            print(f"{'  '*depth}Partitioning: {arr[low:high+1]}, pivot={pivot}")
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                if verbose:
                    print(f"{'  '*depth}Swap arr[{i}] and arr[{j}]: {arr}")
        arr[i+1], arr[high] = arr[high], arr[i+1]
        if verbose:
            print(f"{'  '*depth}Swap pivot arr[{high}] with arr[{i+1}]: {arr}")
        return i+1
    _quicksort(arr, 0, len(arr)-1)
    if verbose:
        print(f"Final sorted array: {arr}")
