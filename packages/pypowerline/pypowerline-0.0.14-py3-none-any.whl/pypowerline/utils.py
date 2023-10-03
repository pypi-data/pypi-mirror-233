def execute_python_file(file_path: str, vals=None):
    try:
        with open(file_path, 'r') as file:
            python_code = file.read()
            # pylint: disable=exec-used
            exec(python_code, globals(), vals)
    except FileNotFoundError:
        print(f"Error: The file [{file_path}] does not exist.")
