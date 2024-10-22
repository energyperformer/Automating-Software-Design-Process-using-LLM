from transformers import GPT2LMHeadModel, GPT2Tokenizer
# import torch
# import requests
# import os
# import subprocess
# import base64
# import zlib
# import urllib.request
# import shutil
# import traceback

model_name = "gpt2"  # Replace with your fine-tuned model name
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)


def generate_use_case_uml(processed_data):
    entities = processed_data.get('entities', [])
    noun_phrases = processed_data.get('noun_phrases', [])
    
    # Extract potential actors and use cases
    actors = list(set([ent[0] for ent in entities if ent[1] in ['PERSON', 'ORG']]))[:5]  # Limit to 5 actors
    use_cases = list(set([np for np in noun_phrases if np.lower().startswith(('manage', 'create', 'update', 'delete', 'view', 'process', 'generate', 'analyze'))][:10]))  # Limit to 10 use cases
    
    # Generate UML code
    uml_code = "@startuml\n"
    
    # Add actors
    for actor in actors:
        actor = actor.replace('"', '').replace('\n', ' ').strip()  # Remove quotes and newlines
        if actor:
            uml_code += f'actor "{actor}"\n'
    
    # Add use cases
    for use_case in use_cases:
        use_case = use_case.replace('"', '').replace('\n', ' ').strip()  # Remove quotes and newlines
        if use_case:
            uml_code += f'usecase "{use_case}"\n'
    
    # Add some connections
    for i, actor in enumerate(actors):
        actor = actor.replace('"', '').replace('\n', ' ').strip()
        for j in range(min(2, len(use_cases))):
            use_case = use_cases[j].replace('"', '').replace('\n', ' ').strip()
            if actor and use_case:
                uml_code += f'"{actor}" --> "{use_case}"\n'
    
    uml_code += "@enduml"
    return uml_code

def generate_uml_code(processed_data):
    return generate_use_case_uml(processed_data)

__all__ = ['generate_uml_code']

# def generate_uml_diagram(uml_code_path, output_path):
#     try:
#         # Ensure plantuml.jar is in the project directory
#         project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
#         plantuml_path = os.path.join(project_root, 'plantuml.jar')
        
#         if not os.path.exists(plantuml_path):
#             print(f"PlantUML jar not found. Attempting to download...")
#             urllib.request.urlretrieve("https://sourceforge.net/projects/plantuml/files/plantuml.jar/download", plantuml_path)
#             print(f"PlantUML jar downloaded to {plantuml_path}")

#         # Ensure the output directory exists
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)

#         # Run plantuml command
#         command = f"java -jar \"{plantuml_path}\" \"{uml_code_path}\" -o \"{os.path.dirname(output_path)}\""
#         print(f"Executing command: {command}")
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)

#         print(f"Command stdout: {result.stdout}")
#         print(f"Command stderr: {result.stderr}")

#         # The output file will have the same name as the input file but with .png extension
#         expected_output_file = os.path.splitext(uml_code_path)[0] + ".png"
        
#         if os.path.exists(expected_output_file):
#             shutil.move(expected_output_file, output_path)
#             print(f"UML diagram generated successfully: {output_path}")
#             return True
#         else:
#             print(f"Failed to generate UML diagram. Output file not found: {expected_output_file}")
#             return False

#     except Exception as e:
#         print(f"Unexpected error generating UML diagram: {str(e)}")
#         traceback.print_exc()
#         return False
