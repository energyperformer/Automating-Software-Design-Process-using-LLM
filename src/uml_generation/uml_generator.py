from transformers import T5Tokenizer, T5ForConditionalGeneration
import os

def load_model():
    """
    Load the fine-tuned T5 model and tokenizer.

    Returns:
    tuple: (model, tokenizer) - The loaded T5 model and tokenizer.

    Raises:
    ValueError: If the model is not found in the specified path.
    """
    model_path = "./models/finetuned_llm"
    if not os.path.exists(model_path):
        raise ValueError("Model not found. Please fine-tune the model first!")
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    return model, tokenizer

def generate_uml_from_srs(srs_text):
    """
    Generate UML code from the given SRS text using the fine-tuned T5 model.

    Args:
    srs_text (str): The input Software Requirements Specification text.

    Returns:
    str: The generated UML code.
    """
    model, tokenizer = load_model()
    inputs = tokenizer.encode("Generate UML for: " + srs_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=512)
    uml_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return uml_code

def process_srs_file(input_file):
    """
    Read an SRS file and generate UML code from its content.

    Args:
    input_file (str): Path to the input SRS text file.

    Returns:
    str: The generated UML code.
    """
    with open(input_file, "r") as f:
        srs_text = f.read()
    uml_code = generate_uml_from_srs(srs_text)
    return uml_code

def save_uml_to_file(uml_code, output_file):
    """
    Save the generated UML code to a file.

    Args:
    uml_code (str): The UML code to be saved.
    output_file (str): Path to the output file where UML code will be saved.
    """
    with open(output_file, "w") as f:
        f.write(uml_code)

if __name__ == "__main__":
    input_file = "data/processed_cleaned/sample_srs.txt"
    output_file = "data/uml/sample_uml.uml"
    
    uml_code = process_srs_file(input_file)
    
    save_uml_to_file(uml_code, output_file)
    print(f"UML code generated and saved to {output_file}")
