import os
import subprocess

def visualize_uml(uml_code_file, output_folder):
    """
    Generate a UML diagram from a PlantUML code file and save it to the specified output folder.

    Args:
    uml_code_file (str): Path to the PlantUML code file.
    output_folder (str): Path to the folder where the generated diagram will be saved.
    """
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        cmd = f"plantuml {uml_code_file} -o {output_folder}"
        
        subprocess.run(cmd, shell=True, check=True)
        
        print(f"Diagram generated and saved in {output_folder}")
    except Exception as e:
        print(f"Error generating UML diagram: {e}")

if __name__ == "__main__":
    uml_code_file = "data/uml/sample_uml.uml"
    output_folder = "diagrams/"
    
    visualize_uml(uml_code_file, output_folder)
