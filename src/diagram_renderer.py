import os
import subprocess

# Specify the path to your Graphviz installation
GRAPHVIZ_PATH = r"C:\Program Files\Graphviz\bin"  # Adjust this path as needed

def render_uml_diagram(uml_code, output_path):
    try:
        # Path to plantuml.jar
        plantuml_path = r"C:\Users\vardh\Downloads\plantuml-jar\plantuml.jar"

        # Create a temporary file for the UML code
        temp_file = "temp_uml.txt"
        with open(temp_file, "w", encoding='utf-8') as f:
            f.write(uml_code)

        # Run plantuml command
        command = f"java -jar {plantuml_path} -tpng {temp_file} -o {os.path.dirname(output_path)}"
        print(f"Executing command: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

        # Remove the temporary file
        os.remove(temp_file)

        if os.path.exists(output_path):
            print(f"UML diagram generated successfully: {output_path}")
            return True
        else:
            print(f"Failed to generate UML diagram. PlantUML output: {result.stdout}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error running PlantUML: {e}")
        print(f"Command output: {e.output}")
        print(f"Command stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error generating UML diagram: {str(e)}")
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



