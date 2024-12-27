import PyPDF2
from huggingface_hub import InferenceClient


def process_srs_document(pdf_path):
    """
    Extract text from a PDF file.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

from huggingface_hub import InferenceClient

# Hugging Face API Token
HUGGINGFACEHUB_API_TOKEN = "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"

# Initialize the Inference Client
client = InferenceClient(
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=HUGGINGFACEHUB_API_TOKEN
)

# Level 1: Identify Actors
def level_1_actors(srs_text):
    prompt = f"""
    Analyze the following SRS document to identify the key actors explicitly or implicitly mentioned.
    List them step-by-step in a simple format.

    SRS Document:
    {srs_text}

    Output:
    Actors:
    1. (Actor 1)
    2. (Actor 2)
    """
    response = client.text_generation(prompt, max_new_tokens=500, temperature=0.7)
    return response.strip()

# Level 2: Identify Use Cases
def level_2_use_cases(srs_text, actors):
    prompt = f"""
    Based on the following SRS document and the identified actors, list the main use cases explicitly or implicitly described.
    List them step-by-step, focusing on functional requirements.

    SRS Document:
    {srs_text}

    Identified Actors:
    {actors}

    Output:
    Use Cases:
    1. (Use Case 1)
    2. (Use Case 2)
    """
    response = client.text_generation(prompt, max_new_tokens=500, temperature=0.7)
    return response.strip()

# Level 3: Establish Relationships
def level_3_relationships(actors, use_cases):
    prompt = f"""
    Based on the identified actors and use cases, determine the relationships between them.
    Specify which actors are associated with which use cases.

    Actors:
    {actors}

    Use Cases:
    {use_cases}

    Output:
    Relationships:
    Actor1 --> UseCase1
    Actor2 --> UseCase2
    """
    response = client.text_generation(prompt, max_new_tokens=500, temperature=0.7)
    return response.strip()

# Level 4: Generate UML Code
def level_4_generate_uml(actors, use_cases, relationships):
    prompt = f"""
    Generate a detailed UML Use Case Diagram in PlantUML syntax based on the provided actors, use cases, and relationships.

    Actors:
    {actors}

    Use Cases:
    {use_cases}

    Relationships:
    {relationships}

    Output:
    @startuml
    actor Actor1
    usecase "Use Case 1" as UC1
    Actor1 --> UC1
    @enduml
    """
    response = client.text_generation(prompt, max_new_tokens=1000, temperature=0.7)
    return response.strip()

# Orchestrating the Levels
def generate_use_case_uml(srs_text):
    try:
        # Level 1: Identify Actors
        actors = level_1_actors(srs_text)
        print("Level 1 - Actors Identified:", actors)

        # Level 2: Identify Use Cases
        use_cases = level_2_use_cases(srs_text, actors)
        print("Level 2 - Use Cases Identified:", use_cases)

        # Level 3: Establish Relationships
        relationships = level_3_relationships(actors, use_cases)
        print("Level 3 - Relationships Established:", relationships)

        # Level 4: Generate UML Code
        uml_code = level_4_generate_uml(actors, use_cases, relationships)
        print("Level 4 - UML Code Generated:\n", uml_code)

        return uml_code
    except Exception as e:
        print("Error during UML generation:", e)
        return None

# # Example SRS Text
# srs_text = """A system for managing appointments and medical records. Key features include:
# - Patients book, update, or cancel appointments.
# - Doctors review medical records.
# - Admins manage patient information."""

# Generate UML Code
pdf_path = "Automating-Software-Design-Process-using-LLM-s/library.pdf"
srs_text = process_srs_document(pdf_path)
uml_output = generate_use_case_uml(srs_text)
# Save UML Code to File
if uml_output:
    with open("use_case_uml_output.txt", "w") as file:
        file.write(uml_output)
    print("UML code saved to use_case_uml_output.txt")
