from huggingface_hub import InferenceClient
import PyPDF2

import re

# Hugging Face API Token
HUGGINGFACEHUB_API_TOKEN = "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"

# Initialize the Inference Client
client = InferenceClient(
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=HUGGINGFACEHUB_API_TOKEN
)

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
# Metrics evaluation functions using LLM
def evaluate_use_case_diagram_with_llm(uml_code):
    """
    Evaluate the UML Use Case Diagram using an LLM.
    """
    prompt = f"""
    You are an expert in evaluating UML diagrams. Analyze the following Use Case Diagram in PlantUML format
    and evaluate it based on the following metrics:

    1. Number of Actors (NA): Count the number of distinct actors.
    2. Number of Use Cases (NUC): Count the number of distinct use cases.
    3. Actor-to-Use Case Ratio (AUC): Compute the ratio of actors to use cases.
    4. Relationships (Include/Extend): Count the number of relationships (arrows) in the diagram.

    Diagram:
    {uml_code}

    Provide your evaluation in the following format:
    Metrics:
    - Number of Actors (NA): <value>
    - Number of Use Cases (NUC): <value>
    - Actor-to-Use Case Ratio (AUC): <value>
    - Relationships (Include/Extend): <value>

    Score:
    <value out of 5>
    """
    
    response = client.text_generation(prompt, max_new_tokens=500, temperature=0.2)

    # Extract metrics and score using regex
    metrics_match = re.search(r"Metrics:\s*([\s\S]*?)Score:", response)
    score_match = re.search(r"Score:\s*(\d+)", response)

    if metrics_match and score_match:
        metrics_text = metrics_match.group(1).strip()
        score = int(score_match.group(1))
        return metrics_text, score
    else:
        return "Evaluation failed", 0

# Feedback Loop for Generating Optimal UML Code
def generate_optimal_use_case_uml(srs_text):
    iteration = 0
    max_iterations = 5
    optimal_score = 4  # Define the desired score threshold

    while iteration < max_iterations:
        iteration += 1

        # Generate UML Code
        prompt = f"""
        You are an expert UML designer. Analyze the following SRS document and generate a Use Case Diagram.
        Focus on defining actors, use cases, and their relationships accurately.

        SRS Document:
        {srs_text}

        Output:
        @startuml
        actor Actor1
        usecase "Use Case 1" as UC1
        Actor1 --> UC1
        @enduml
        """
        
        response = client.text_generation(prompt, max_new_tokens=1000, temperature=0.7)
        uml_code = extract_uml_code(response)

        # Evaluate the generated UML code using LLM
        metrics, score = evaluate_use_case_diagram_with_llm(uml_code)
        print(f"Iteration {iteration} - Score: {score}")
        print("Metrics:", metrics)

        # If score meets the optimal threshold, return the UML code
        if score >= optimal_score:
            print("Optimal UML code generated.")
            return uml_code

        # Provide feedback and iterate
        feedback_prompt = f"""
        The following UML Use Case Diagram was generated:
        {uml_code}

        The evaluation metrics are as follows:
        {metrics}

        The score is {score}, which is below the desired threshold of {optimal_score}.
        Please refine the diagram by:
        - Ensuring all actors and use cases are properly defined.
        - Adding missing relationships or refining existing ones.

        Generate a revised UML Use Case Diagram.
        """
        response = client.text_generation(feedback_prompt, max_new_tokens=1000, temperature=0.7)
        uml_code = extract_uml_code(response)

    print("Max iterations reached. Returning the best attempt.")
    return uml_code

# Extract UML code from response
def extract_uml_code(response_text):
    start_idx = response_text.find("@startuml")
    end_idx = response_text.find("@enduml") + len("@enduml")

    if start_idx != -1 and end_idx != -1:
        return response_text[start_idx:end_idx].strip()
    else:
        return "No valid UML code found."

# Example SRS Text
srs_text = """A system for managing appointments and medical records. Key features include:
- Patients book, update, or cancel appointments.
- Doctors review medical records.
- Admins manage patient information."""

# Generate UML Code with Feedback Loop
pdf_path = "Automating-Software-Design-Process-using-LLM-s/library.pdf"
srs_text = process_srs_document(pdf_path)
# uml_output = generate_use_case_uml(srs_text)
uml_output = generate_optimal_use_case_uml(srs_text)

# Save UML Code to File
if uml_output:
    with open("optimal_use_case_uml_output.txt", "w") as file:
        file.write(uml_output)
    print("UML code saved to optimal_use_case_uml_output.txt")
