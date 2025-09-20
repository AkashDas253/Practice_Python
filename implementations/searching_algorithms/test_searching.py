
from algorithms.linear_search import linear_search
from algorithms.binary_search import binary_search
from algorithms.jump_search import jump_search
from algorithms.exponential_search import exponential_search

test_cases = [
    ([1, 3, 5, 7, 9, 11], 7, 3),
    ([1, 3, 5, 7, 9, 11], 4, -1),
    ([5, 2, 9, 1, 5, 6], 9, 2),
    ([10, 20, 30, 40], 20, 1),
    ([10, 20, 30, 40], 50, -1)
]

def run_tests():
    algos = [
        ("Linear Search", linear_search),
        ("Binary Search", binary_search),
        ("Jump Search", jump_search),
        ("Exponential Search", exponential_search)
    ]
    for name, func in algos:
        print(f"{name}:")
        for i, (arr, target, expected) in enumerate(test_cases):
            result = func(arr, target, verbose=False)
            print(f"  Test {i+1}: Array={arr}, Target={target}", end=" ")
            print("PASS" if result == expected else f"FAIL (got {result}, expected {expected})")
        print()

if __name__ == "__main__":
    run_tests()
