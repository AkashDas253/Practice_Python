def heapsort(arr, verbose=False):
    def heapify(arr, n, i, depth=1):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            if verbose:
                print(f"{'  '*depth}Swap arr[{i}] and arr[{largest}]: {arr}")
            heapify(arr, n, largest, depth+1)
    n = len(arr)
    if verbose:
        print(f"Building max heap: {arr}")
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)
    if verbose:
        print(f"Max heap built: {arr}")
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        if verbose:
            print(f"Swap arr[0] and arr[{i}]: {arr}")
        heapify(arr, i, 0)
    if verbose:
        print(f"Final sorted array: {arr}")
