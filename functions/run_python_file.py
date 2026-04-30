import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file]
    if args:
        command.extend(args)
    try:
       # Execute the process with the specified constraints
        result = subprocess.run(
            command, 
            cwd=working_dir_abs, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        output_parts = []
        # Check for non-zero exit code
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        # Check for output and build strings
        if not result.stdout.strip() and not result.stderr.strip():
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR: {result.stderr}")
        return "\n".join(output_parts)
    except subprocess.TimeoutExpired:
        return "Error: The process timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"