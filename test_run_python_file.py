import os
from functions.run_python_file import run_python_file

def run_tests():
    print("--- Starting Tests for run_python_file ---\n")

    # Test Case 1: Run calculator without args (Usage instructions)
    print("Test 1: Basic execution")
    print(run_python_file("calculator", "main.py"))
    print("-" * 30)

    # Test Case 2: Run calculator with valid calculation
    print("Test 2: Execution with arguments")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("-" * 30)

    # Test Case 3: Run internal tests
    print("Test 3: Running internal tests.py")
    print(run_python_file("calculator", "tests.py"))
    print("-" * 30)

    # Test Case 4: Directory traversal attempt (Should error)
    print("Test 4: Security check (outside directory)")
    print(run_python_file("calculator", "../main.py"))
    print("-" * 30)

    # Test Case 5: Missing file (Should error)
    print("Test 5: Non-existent file")
    print(run_python_file("calculator", "nonexistent.py"))
    print("-" * 30)

    # Test Case 6: Invalid file type (Should error)
    print("Test 6: Wrong file extension")
    print(run_python_file("calculator", "lorem.txt"))
    print("-" * 30)

if __name__ == "__main__":
    run_tests()
