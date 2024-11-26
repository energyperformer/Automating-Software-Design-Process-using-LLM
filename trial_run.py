# import PyPDF2
# from huggingface_hub import InferenceClient

# # Hugging Face API token
# HUGGINGFACEHUB_API_TOKEN = "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"

# # Initialize the Inference Client
# client = InferenceClient(
#     model="Qwen/Qwen2.5-Coder-32B-Instruct", 
#     token=HUGGINGFACEHUB_API_TOKEN
# )

# def process_srs_document(pdf_path):
#     """
#     Extract text from a PDF file.
#     """
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
#     return text

# def construct_prompt_for_uml(srs_text):
#     """
#     Construct a well-engineered prompt for generating PlantUML code.
#     """
#     prompt = f"""
# You are an expert in software design. Analyze the following Software Requirements Specification (SRS) and generate a UML use case diagram in PlantUML format.

# SRS Document:
# {srs_text}

# Steps:
# 1. Identify key actors based on the SRS (e.g., users, systems).
# 2. Identify use cases from functional requirements.
# 3. Link actors to use cases using relationships.
# 4. Provide the output ONLY in PlantUML format, with no additional explanations or comments.

# Example format:
# @startuml
# actor Actor1
# actor Actor2
# usecase "Use Case 1" as UC1
# usecase "Use Case 2" as UC2
# Actor1 --> UC1
# Actor2 --> UC2
# @enduml

# Now generate the UML diagram based on the SRS provided.
# """
#     return prompt

# def generate_uml_code(pdf_path):
#     """
#     Process the PDF, construct the prompt, and get UML code using the LLM.
#     """
#     # Extract text from the PDF
#     srs_text = process_srs_document(pdf_path)
    
#     # Construct the prompt
#     prompt = construct_prompt_for_uml(srs_text)
    
#     # Call the LLM
#     try:
#         response = client.text_generation(
#             prompt,
#             max_new_tokens=1000,  # Adjust token limit based on your requirements
#             temperature=0.7
#         )
#         uml_code = extract_uml_code(response)  # Extract PlantUML code only
#         print(uml_code)
#         return uml_code
#     except Exception as e:
#         print("Error during UML generation:", e)
#         return None

# def extract_uml_code(response_text):
#     """
#     Extract and return only the UML code from the response.
#     """
#     start_idx = response_text.find("@startuml")
#     end_idx = response_text.find("@enduml") + len("@enduml")
    
#     if start_idx != -1 and end_idx != -1:
#         return response_text[start_idx:end_idx].strip()
#     else:
#         return "No valid UML code found."

# # Example usage


# # Example usage
# pdf_path = "Automating-Software-Design-Process-using-LLM-s/gamma.pdf"
# uml_code = generate_uml_code(pdf_path)

# if uml_code:
#     with open("uml_data_output.txt", "w") as output_file:
#         output_file.write(uml_code)
#     print("UML code saved to uml_output.txt")

from huggingface_hub import InferenceClient

# Hugging Face API token
HUGGINGFACEHUB_API_TOKEN = "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"

# Initialize Inference Client for CodeT5
# Initialize Inference Client for StarCoder
# client = InferenceClient(
#     model="bigcode/starcoder",
#     token=HUGGINGFACEHUB_API_TOKEN
# )

# # Example Usage
# prompt = "Generate a UML Code plantuml based UML Activity Diagram for a shopping cart system."
# response = client.text_generation(prompt, max_new_tokens=1000, temperature=0.7)

# print("Generated UML Code:")
# print(response)

# Initialize Inference Client for Falcon
# Initialize Inference Client for LLaMA
# Initialize Inference Client for OpenAssistant
client = InferenceClient(
    model="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
    token=HUGGINGFACEHUB_API_TOKEN
)

# Example Usage
prompt = "Generate a UML Class Diagram for a Library System where members borrow books and librarians manage inventory."
response = client.text_generation(prompt, max_new_tokens=1000, temperature=0.7)

print("Generated UML Code:")
print(response)

