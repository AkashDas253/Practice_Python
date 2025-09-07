from selection_sort import selection_sort
from insertion_sort import insertion_sort
from bubble_sort import bubble_sort
from quicksort import quicksort
from mergesort import mergesort
from heapsort import heapsort

def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

test_cases = [
    [5, 2, 9, 1, 5, 6],
    [3, 7, 0, -1, 8],
    [1],
    [],
    [10, 9, 8, 7, 6]
]
expected = [
    [1, 2, 5, 5, 6, 9],
    [-1, 0, 3, 7, 8],
    [1],
    [],
    [6, 7, 8, 9, 10]
]

def run_tests():
    algos = [
        ("SelectionSort", selection_sort),
        ("InsertionSort", insertion_sort),
        ("BubbleSort", bubble_sort),
        ("HeapSort", heapsort),
        ("QuickSort", quicksort),
        ("MergeSort", mergesort)
    ]
    for name, func in algos:
        print(f"{name}:")
        for i, arr in enumerate(test_cases):
            arr_copy = arr.copy()
            func(arr_copy, verbose=False)
            print("Sorted array:", arr_copy)
            print(f"  Test {i+1}:", "PASS" if arr_copy == expected[i] else "FAIL")
        print()

if __name__ == "__main__":
    run_tests()
