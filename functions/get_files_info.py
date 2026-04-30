

import os


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_directory = os.path.commonpath([working_dir_abs, target_directory]) == working_dir_abs
    if not valid_target_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'
    try:
        files_info = []
        for entry in os.listdir(target_directory):
            entry_path = os.path.join(target_directory, entry)
            size = os.path.getsize(entry_path)
            files_info.append(f"- {entry}: file_size={size} bytes, is_dir={os.path.isdir(entry_path)}")
        return "\n".join(files_info) if files_info else "Error: No files found in the directory."
    except Exception as e:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory. Details: {str(e)}'