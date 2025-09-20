import math

def jump_search(arr, target, verbose=False):
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    if verbose:
        print(f"Jump step: {step}")
    while prev < n and arr[min(step, n)-1] < target:
        if verbose:
            print(f"Jumping from {prev} to {min(step, n)-1}")
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    for i in range(prev, min(step, n)):
        if verbose:
            print(f"Checking index {i}: {arr[i]}")
        if arr[i] == target:
            return i
    return -1
