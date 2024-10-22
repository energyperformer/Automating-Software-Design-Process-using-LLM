import os
import subprocess
import urllib.request
import shutil
import traceback


def generate_uml_diagram(uml_code_path, output_path):
    try:
        # Ensure plantuml.jar is in the project directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        plantuml_path = os.path.join(project_root, 'plantuml.jar')
        
        if not os.path.exists(plantuml_path):
            print(f"PlantUML jar not found. Attempting to download...")
            urllib.request.urlretrieve("https://sourceforge.net/projects/plantuml/files/plantuml.jar/download", plantuml_path)
            print(f"PlantUML jar downloaded to {plantuml_path}")

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Run plantuml command
        command = f"java -jar \"{plantuml_path}\" \"{uml_code_path}\" -o \"{os.path.dirname(output_path)}\""
        # print(f"Executing command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # print(f"Command stdout: {result.stdout}")
        # print(f"Command stderr: {result.stderr}")

        # The output file will have the same name as the input file but with .png extension
        expected_output_file = os.path.splitext(uml_code_path)[0] + ".png"
        
        if os.path.exists(expected_output_file):
            shutil.move(expected_output_file, output_path)
            print('*'*10)
            print(f"UML diagram generated successfully: {output_path}")
            return True
        else:
            print(f"Failed to generate UML diagram. Output file not found: {expected_output_file}")
            return False

    except Exception as e:
        print(f"Unexpected error generating UML diagram: {str(e)}")
        traceback.print_exc()
        return False





















# import os
# import requests
# import zlib
# import base64

# def encode_plantuml(text):
#     """
#     Encode the UML code for PlantUML URL using DEFLATE and add the ~1 header.
#     """
#     compressed = zlib.compress(text.encode('utf-8'))
#     compressed = compressed[2:-4]  # Remove zlib header and checksum
#     encoded = base64.b64encode(compressed).decode('utf-8')
#     return f"~1{encoded.replace('=', '')}"

# def render_uml_diagram(uml_code, output_path):
#     try:
#         # Encode the UML code
#         encoded = encode_plantuml(uml_code)
        
#         # Make a request to the PlantUML server
#         url = f"http://www.plantuml.com/plantuml/png/{encoded}"
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             # Save the image
#             with open(output_path, 'wb') as f:
#                 f.write(response.content)
#             print(f"UML diagram generated and saved to {output_path}")
#             print(f"URL used: {url}")
#             return True
#         else:
#             print(f"Failed to generate UML diagram. Server returned status code: {response.status_code}")
#             print(f"URL used: {url}")
#             return False
#     except Exception as e:
#         print(f"Unexpected error generating UML diagram: {e}")
#         return False



