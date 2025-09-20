def insertion_sort(arr, verbose=False):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        if verbose:
            print(f"Step {i}:")
            print(f"  Key = {key}")
        while j >= 0 and arr[j] > key:
            if verbose:
                print(f"    arr[{j}] ({arr[j]}) > key ({key}), shifting arr[{j}] to arr[{j+1}]")
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        if verbose:
            print(f"  Insert key at arr[{j+1}]")
            print(f"  Array after step {i}: {arr}")
    if verbose:
        print(f"Final sorted array: {arr}")
