import os
from functions.get_file_content import get_file_content
from config import MAX_CHARS

def test_get_file_content():
    lorem_path = os.path.join("calculator", "lorem.txt")
    try:
        with open(lorem_path, "r", encoding="utf-8") as lorem_file:
            full_lorem = lorem_file.read()
    except Exception as error:
        full_lorem = ""
        print(f"ERROR: Could not read lorem.txt for validation: {error}")

    print(f"lorem.txt actual length: {len(full_lorem)}")
    print(f"MAX_CHARS: {MAX_CHARS}")
    if len(full_lorem) <= MAX_CHARS:
        print("WARNING: lorem.txt is not longer than MAX_CHARS; truncation will not be tested.")
    else:
        print("lorem.txt is longer than MAX_CHARS; truncation should occur.")

    result = get_file_content('calculator', 'lorem.txt')
    print(f"length of result: {len(result)}")
    if '[...File "lorem.txt" truncated' in result:
        truncation_notice = result[result.rfind('[...'):]
        print("Result (truncation notice):")
        print(truncation_notice)
    else:
        print("Result:")
        print(result[-200:] if len(result) > 200 else result)

    result = get_file_content("calculator", "main.py")
    print(f"length of content: {len(result)}\nTruncated content:\n{result}")
    result = get_file_content("calculator", "pkg/calculator.py")
    print(f"length of result: {len(result)}\nResult:\n{result}")
    result = get_file_content("calculator", "/bin/cat")
    print(f"length of result: {len(result)}\nResult:\n{result}")
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(f"length of result: {len(result)}\nResult:\n{result}")

test_get_file_content()