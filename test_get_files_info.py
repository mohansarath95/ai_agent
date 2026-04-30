from functions.get_files_info import get_files_info

def test_get_files_info():
    print(f"Result for current directory:\n {get_files_info('calculator', '.')}")
    print(f"\nResult for 'pkg' directory:\n {get_files_info('calculator', 'pkg')}")
    print(f"\nResult for '/bin' directory:\n {get_files_info('calculator', '/bin')}")
    print(f"\nResult for '..' directory:\n {get_files_info('calculator', '..')}")
    
test_get_files_info()
