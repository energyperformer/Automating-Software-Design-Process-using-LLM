import os

def save_file(text, file_path):
    """
    Save the given text to a file at the  path.

    Args:
    text (str): The content to be saved to the file.
    file_path (str): The path where the file should be saved.

    Prints:
    A success message if the file is saved successfully, or an error message.
    """
    try:
        with open(file_path, "w") as f:
            f.write(text)
        print(f"File saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
        

def read_file(file_path):
    """
    Read and return the contents of a file at the specified path.

    Args:
    file_path (str): The path of the file to be read.

    Returns:
    str: The contents of the file if successfully read.

    Prints:
    An error message if an exception occurs while reading the file.
    """
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
