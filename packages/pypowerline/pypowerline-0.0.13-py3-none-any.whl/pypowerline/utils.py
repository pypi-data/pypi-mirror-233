def execute_python_file(file_path: str):
   try:
      with open(file_path, 'r') as file:
         python_code = file.read()
         exec(python_code)
   except FileNotFoundError:
      print(f"Error: The file '{file_path}' does not exist.")
