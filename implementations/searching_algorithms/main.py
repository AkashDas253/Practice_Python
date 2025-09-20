# main.py for searching_algorithms
# Example usage of search algorithms
from algorithms.linear_search import linear_search
from algorithms.binary_search import binary_search
from algorithms.jump_search import jump_search
from algorithms.exponential_search import exponential_search

def get_array():
    choice = input("Use default array [1, 3, 5, 7, 9, 11]? (y/n): ").strip().lower()
    if choice == 'y':
        return [1, 3, 5, 7, 9, 11]
    else:
        arr_str = input("Enter array elements separated by spaces: ")
        return [int(x) for x in arr_str.strip().split() if x]

def main():
    print("Choose searching algorithm:")
    print("1. Linear Search")
    print("2. Binary Search")
    print("3. Jump Search")
    print("4. Exponential Search")
    algo_choice = input("Enter choice: ").strip()
    arr = get_array()
    target = int(input("Enter target value to search for: ").strip())
    verbose = input("Show step-by-step working? (y/n): ").strip().lower() == 'y'
    print(f"Array: {arr}")
    idx = -1
    if algo_choice == '1':
        idx = linear_search(arr, target, verbose)
        print(f"Linear Search: Index {idx}" if idx != -1 else "Linear Search: Not found")
    elif algo_choice == '2':
        idx = binary_search(arr, target, verbose)
        print(f"Binary Search: Index {idx}" if idx != -1 else "Binary Search: Not found")
    elif algo_choice == '3':
        idx = jump_search(arr, target, verbose)
        print(f"Jump Search: Index {idx}" if idx != -1 else "Jump Search: Not found")
    elif algo_choice == '4':
        idx = exponential_search(arr, target, verbose)
        print(f"Exponential Search: Index {idx}" if idx != -1 else "Exponential Search: Not found")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
