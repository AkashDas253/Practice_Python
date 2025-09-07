def selection_sort(arr, verbose=False):
    n = len(arr)
    for i in range(n):
        min_idx = i
        if verbose:
            print(f"Step {i+1}:")
            print(f"  Start index {i}, current value: {arr[i]}")
        for j in range(i+1, n):
            if verbose:
                print(f"    Compare arr[{j}] ({arr[j]}) with current min arr[{min_idx}] ({arr[min_idx]})")
            if arr[j] < arr[min_idx]:
                min_idx = j
                if verbose:
                    print(f"    New min found at index {min_idx} ({arr[min_idx]})")
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            if verbose:
                print(f"  Swap arr[{i}] ({arr[min_idx]}) with arr[{min_idx}] ({arr[i]})")
        else:
            if verbose:
                print(f"  No swap needed for index {i}")
        if verbose:
            print(f"  Array after step {i+1}: {arr}")
    if verbose:
        print(f"Final sorted array: {arr}")
