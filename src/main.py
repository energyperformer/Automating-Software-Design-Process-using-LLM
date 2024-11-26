import os

import random
from data_processing.pdf_extractor import process_srs_document
from nlp.nlp_pipeline import process_text
from uml_generation.uml_generator import generate_uml_code
from diagram_renderer import generate_uml_diagram


def save_uml_code(uml_code, output_path):
    output_path = os.path.splitext(output_path)[0] + '.puml'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(uml_code)
    print(f"Use case UML code saved to {output_path}")
    return output_path  

def main():
    raw_data_dir = os.path.join("data", "raw")
    pdf_files = [f for f in os.listdir(raw_data_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the data/raw directory.")
        return
    
    # Select a random PDF file
    selected_pdf = random.choice(pdf_files)
    pdf_path = os.path.join(raw_data_dir, selected_pdf)
    
    base_filename = os.path.splitext(selected_pdf)[0]
    uml_code_filename = f"{base_filename}_use_case_uml_code.puml"
    uml_diagram_filename = f"{base_filename}_use_case_diagram.png"
    
    uml_code_path = os.path.join("data", "processed", uml_code_filename)
    uml_diagram_path = os.path.join("data", "processed", uml_diagram_filename)
    
    try:
        # Extract text from PDF
        
        print(f"Processing {selected_pdf}...")
        srs_text = process_srs_document(pdf_path)
        print(f"Extracted {len(srs_text)} characters from the PDF.")
        srs_text_path = "srs_text_output.txt"
        with open(srs_text_path, "w", encoding="utf-8") as file:
            file.write(srs_text)
        print(f"SRS text saved to {srs_text_path}")
        
        # Process text with NLP pipeline
        # processed_data = process_text(srs_text)
        
        # After processing the text with the NLP pipeline

# Save processed_data to a text file, converting it to a JSON string
        # processed_data_path = "processed_data_output.txt"
        # with open(processed_data_path, "w", encoding="utf-8") as file:
        #     file.write(json.dumps(processed_data, indent=4))
        # print(f"Processed data saved to {processed_data_path}")

        
        # Generate UML code
        uml_code = generate_uml_code(srs_text)
        print(f"Generated use case UML code of length {len(uml_code)}.")
        uml_data_path = "uml_data_output.txt"
        with open(uml_data_path, "w", encoding="utf-8") as file:
            file.write(uml_code)
        print(f"Processed data saved to {uml_data_path}")
        
        # Save UML code
        uml_code_path = os.path.abspath(os.path.join('data', 'processed', f"{os.path.splitext(os.path.basename(pdf_path))[0]}_use_case_uml_code.puml"))
        with open(uml_code_path, 'w', encoding='utf-8') as f:
            f.write(uml_code)
        print('*'*10)
        print(f"Use case UML code saved to {uml_code_path}")

        # Generate UML diagram
        uml_diagram_path = os.path.abspath(os.path.join('data', 'processed', f"{os.path.splitext(os.path.basename(pdf_path))[0]}_use_case_diagram.png"))
        if generate_uml_diagram(uml_code_path, uml_diagram_path):
            # print(f"Use case diagram generated and saved to {uml_diagram_path}")
            pass
        else:
            print("Failed to generate use case diagram.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())
        print("Please make sure all dependencies are installed correctly.")


if __name__ == "__main__":
    main()
