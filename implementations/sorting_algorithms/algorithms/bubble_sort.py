def bubble_sort(arr, verbose=False):
    n = len(arr)
    for i in range(n):
        swapped = False
        if verbose:
            print(f"Pass {i+1}:")
        for j in range(0, n-i-1):
            if verbose:
                print(f"  Compare arr[{j}] ({arr[j]}) and arr[{j+1}] ({arr[j+1]})")
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
                if verbose:
                    print(f"    Swap arr[{j}] and arr[{j+1}]: {arr}")
        if verbose:
            print(f"  Array after pass {i+1}: {arr}")
        if not swapped:
            if verbose:
                print("  No swaps, array is sorted.")
            break
    if verbose:
        print(f"Final sorted array: {arr}")
