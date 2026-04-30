from functions.write_file import write_file

def test_write_file():
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(f"Test 1 - Overwrite lorem.txt:\n{result}\n")
    
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(f"Test 2 - Write to new file in pkg directory:\n{result}\n")
    
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(f"Test 3 - Attempt to write outside working directory:\n{result}\n")

test_write_file()
