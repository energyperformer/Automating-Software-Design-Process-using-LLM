import os

import random
from data_processing.pdf_extractor import process_srs_document
from nlp.nlp_pipeline import process_text
from uml_generation.uml_generator import generate_uml_code,generate_class_diagram_code,generate_activity_diagram_code
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
    selected_pdf = "0000 - inventory.pdf"
    # print(selected_pdf,"hello")
    # selected_pdf="Automating-Software-Design-Process-using-LLM-s/src/library.pdf"
    pdf_path = os.path.join(raw_data_dir, selected_pdf)
    
    base_filename = os.path.splitext(selected_pdf)[0]
    uml_code_filename = f"{base_filename}_use_case_uml_code.puml"
    uml_diagram_filename = f"{base_filename}_use_case_diagram.png"
    
    uml_code_path = os.path.join("Data", "processed", uml_code_filename)
    uml_diagram_path = os.path.join("Data", "processed", uml_diagram_filename)
    
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

        


        # use_case_uml_code = generate_uml_code(srs_text)
        # print(f"Generated Use Case UML code of length {len(use_case_uml_code)}.")

        # use_case_uml_path = os.path.abspath(os.path.join('Data', 'processed', f"{os.path.splitext(os.path.basename(pdf_path))[0]}_use_case_uml_code.puml"))
        # with open(use_case_uml_path, 'w', encoding='utf-8') as file:
        #     file.write(use_case_uml_code)
        # print(f"Use Case UML code saved to {use_case_uml_path}")

        # Generate and save Activity Diagram UML code
        # activity_uml_code = generate_activity_diagram_code(srs_text)
        # print(f"Generated Activity Diagram UML code of length {len(activity_uml_code)}.")

        # activity_uml_path = os.path.abspath(os.path.join('Data', 'processed', f"{os.path.splitext(os.path.basename(pdf_path))[0]}_activity_uml_code.puml"))
        # with open(activity_uml_path, 'w', encoding='utf-8') as file:
        #     file.write(activity_uml_code)
        # print(f"Activity Diagram UML code saved to {activity_uml_path}")

        # Generate and save Class Diagram UML code
        class_uml_code = generate_class_diagram_code(srs_text)
        print(f"Generated Class Diagram UML code of length {len(class_uml_code)}.")

        class_uml_path = os.path.abspath(os.path.join('Data', 'processed', f"{os.path.splitext(os.path.basename(pdf_path))[0]}_class_uml_code.puml"))
        with open(class_uml_path, 'w', encoding='utf-8') as file:
            file.write(class_uml_code)
        print(f"Class Diagram UML code saved to {class_uml_path}")

        # # Generate diagrams for Use Case, Activity, and Class UML
        # use_case_diagram_path = os.path.abspath(os.path.join('Data', 'processed', f"{os.path.splitext(os.path.basename(pdf_path))[0]}_use_case_diagram.png"))
        # if generate_uml_diagram(use_case_uml_path, use_case_diagram_path):
        #     print(f"Use Case diagram generated and saved to {use_case_diagram_path}")
        # else:
        #     print("Failed to generate Use Case diagram.")

        # activity_diagram_path = os.path.abspath(os.path.join('Data', 'processed', f"{os.path.splitext(os.path.basename(pdf_path))[0]}_activity_diagram.png"))
        # if generate_uml_diagram(activity_uml_path, activity_diagram_path):
        #     print(f"Activity diagram generated and saved to {activity_diagram_path}")
        # else:
        #     print("Failed to generate Activity diagram.")

        class_diagram_path = os.path.abspath(os.path.join('Data', 'processed', f"{os.path.splitext(os.path.basename(pdf_path))[0]}_class_diagram.png"))
        if generate_uml_diagram(class_uml_path, class_diagram_path):
            print(f"Class diagram generated and saved to {class_diagram_path}")
        else:
            print("Failed to generate Class diagram.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())
        print("Please make sure all dependencies are installed correctly.")


if __name__ == "__main__":
    main()
