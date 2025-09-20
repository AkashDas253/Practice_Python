from algorithms.selection_sort import selection_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.bubble_sort import bubble_sort
from algorithms.quicksort import quicksort
from algorithms.mergesort import mergesort
from algorithms.heapsort import heapsort

def get_array():
    choice = input("Use default array [64, 25, 12, 22, 11]? (y/n): ").strip().lower()
    if choice == 'y':
        return [64, 25, 12, 22, 11]
    else:
        arr_str = input("Enter array elements separated by spaces: ")
        return [int(x) for x in arr_str.strip().split() if x]

def main():
    print("Choose sorting algorithm:")
    print("1. Selection Sort")
    print("2. Insertion Sort")
    print("3. Bubble Sort")
    print("4. QuickSort")
    print("5. MergeSort")
    print("6. HeapSort")
    algo_choice = input("Enter choice: ").strip()
    arr = get_array()
    verbose = input("Show step-by-step working? (y/n): ").strip().lower() == 'y'
    print(f"Initial array: {arr}")
    if algo_choice == '1':
        selection_sort(arr, verbose)
    elif algo_choice == '2':
        insertion_sort(arr, verbose)
    elif algo_choice == '3':
        bubble_sort(arr, verbose)
    elif algo_choice == '4':
        quicksort(arr, verbose)
    elif algo_choice == '5':
        mergesort(arr, verbose)
    elif algo_choice == '6':
        heapsort(arr, verbose)
    else:
        print("Invalid choice.")
        return
    if not verbose:
        print(f"Sorted array: {arr}")

if __name__ == "__main__":
    main()
