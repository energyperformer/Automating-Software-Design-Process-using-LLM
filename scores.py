import re
from huggingface_hub import InferenceClient

# Hugging Face API token
HUGGINGFACEHUB_API_TOKEN = "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"

# Initialize the Inference Client
client = InferenceClient(
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=HUGGINGFACEHUB_API_TOKEN
)

def evaluate_use_case_diagram_with_llm(uml_code):
    """
    Evaluate the UML Use Case Diagram using an LLM with enhanced scoring and metrics evaluation.

    Parameters:
        uml_code (str): The PlantUML code for the Use Case Diagram.

    Returns:
        tuple: A tuple containing the evaluation metrics and total score.
    """
    prompt = f"""
    You are an expert in evaluating UML diagrams. Analyze the following Use Case Diagram in PlantUML format
    and evaluate it based on the following metrics and scoring rules:

    1. Number of Actors (NA):
       - Ideal Range: 2-7.
       - Scoring:
         - 2-7 actors: +1 point.
         - 1 actor: 0 points.
         - >7 actors: +0.5 point.

    2. Number of Use Cases (NUC):
       - Ideal Range: 5-15.
       - Scoring:
         - 5-15 use cases: +1 point.
         - <5 use cases: +0.5 point.
         - >15 use cases: +0.5 point.

    3. Actor-to-Use Case Ratio (AUC):
       - Ideal Ratio: Between 1:3 and 1:7.
       - Scoring:
         - 1:3 to 1:7: +1 point.
         - <1:3: +0.5 point.
         - >1:7: +0.5 point.

    4. Relationships (Include/Extend):
       - Ideal Range: 10-20 relationships.
       - Scoring:
         - 10-20 relationships: +1 point.
         - <10 relationships: +0.5 point.
         - >20 relationships: +0.5 point.

    Diagram:
    {uml_code}

    Based on these rules, provide the evaluation in the following format:
    Metrics:
    - Number of Actors (NA): <value> (Score: <score>)
    - Number of Use Cases (NUC): <value> (Score: <score>)
    - Actor-to-Use Case Ratio (AUC): <value> (Score: <score>)
    - Relationships (Include/Extend): <value> (Score: <score>)

    Total Score: <value out of 5>
    """

    response = client.text_generation(prompt, max_new_tokens=1000, temperature=0.2)

    # Extract metrics and score using regex
    metrics_match = re.search(r"Metrics:\s*([\s\S]*?)Total Score:", response)
    score_match = re.search(r"Total Score:\s*(\d+(\.\d+)?)", response)

    if metrics_match and score_match:
        metrics_text = metrics_match.group(1).strip()
        score = float(score_match.group(1))
        return metrics_text, score
    else:
        return "Evaluation failed", 0

# Example usage
if __name__ == "__main__":
    uml_code = """
    @startuml
actor "University administrators" as UA
actor "Faculty administrators" as FA
actor "Department administrators" as DA
actor "Inventory administrators" as IA
actor "Users" as U
actor "IT team system administrators" as ITSA
actor "Inventory system" as IS
actor "Authentication system" as AS

usecase "Transferring Assets" as TA
usecase "Editing Assets" as EA
usecase "Modifying Assets" as MA
usecase "Adding Inventory Assets" as AIA
usecase "Creating Request to Borrow an Asset or Reserve a Space" as CRB
usecase "Returning Assets" as RA
usecase "Creating a New Space" as CNS
usecase "Approving Requests" as AR
usecase "Authentication" as Auth
usecase "Changing Permissions" as CP
usecase "Output Reports" as OR
usecase "Search" as S

UA --> TA
UA --> EA
UA --> MA
UA --> AIA
UA --> AR
UA --> CP
UA --> OR

FA --> TA
FA --> EA
FA --> MA
FA --> AIA
FA --> AR
FA --> CP
FA --> OR

DA --> TA
DA --> EA
DA --> MA
DA --> AIA
DA --> AR
DA --> CP
DA --> OR

IA --> TA
IA --> EA
IA --> MA
IA --> AIA
IA --> RA
IA --> AR
IA --> OR

U --> CRB
U --> S
U --> OR

ITSA --> CNS
ITSA --> Auth
ITSA --> CP

IS --> TA
IS --> EA
IS --> MA
IS --> AIA
IS --> RA

AS --> Auth
@enduml
    """

    metrics, total_score = evaluate_use_case_diagram_with_llm(uml_code)
    print("Evaluation Metrics:")
    print(metrics)
    print("\nTotal Score:", total_score)
