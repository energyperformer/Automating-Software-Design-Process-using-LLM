import re
import os  

def clean_text(text):
    """
    Clean the input text by removing unnecessary characters and having a fixed whitespace.

    Args:
    text (str): The input text that need  to be cleaned.

    Returns:
    str: The cleaned text.
    """
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text

def preprocess_srs_file(input_file, output_file):
    """
    Preprocess a single Software Requirements Specification  file.

    Args:
    input_file (str): Path to the input text file.
    output_file (str): Path where the cleaned text will be saved.
    """
    with open(input_file, "r") as f:
        text = f.read()
    
    cleaned_text = clean_text(text)
    
    with open(output_file, "w") as f:
        f.write(cleaned_text)

def preprocess_all_srs(input_folder, output_folder):
    """
    Preprocess all SRS files in the input folder and save the cleaned versions in the output folder.

    Args:
    input_folder (str): Path to the folder containing the input text files.
    output_folder (str): Path to the folder where cleaned files will be saved.
    """
    for txt_file in os.listdir(input_folder):
        if txt_file.endswith(".txt"):
            input_file = os.path.join(input_folder, txt_file)
            output_file = os.path.join(output_folder, txt_file)
            preprocess_srs_file(input_file, output_file)

if __name__ == "__main__":
    preprocess_all_srs('data/processed/', 'data/processed_cleaned/')
