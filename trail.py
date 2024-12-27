from huggingface_hub import InferenceClient
import PyPDF2
import re
from typing import Tuple, Dict
import json

# Hugging Face API Token
HUGGINGFACEHUB_API_TOKEN = "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"

# Initialize the Inference Client
client = InferenceClient(
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=HUGGINGFACEHUB_API_TOKEN
)

def process_srs_document(pdf_path: str) -> str:
    """
    Extract text from a PDF file with error handling.
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return ""

def get_evaluation_template():
    """
    Returns the evaluation template for metrics.
    """
    return '''
    {
        "metrics": {
            "actor_analysis": {
                "score": 0,
                "details": {
                    "actor_count": 0,
                    "naming_quality": "needs_improvement",
                    "issues": []
                }
            },
            "use_case_quality": {
                "score": 0,
                "details": {
                    "use_case_count": 0,
                    "naming_quality": "needs_improvement",
                    "issues": []
                }
            },
            "relationship_accuracy": {
                "score": 0,
                "details": {
                    "association_count": 0,
                    "include_count": 0,
                    "extend_count": 0,
                    "generalization_count": 0,
                    "issues": []
                }
            },
            "system_boundary": {
                "score": 0,
                "details": {
                    "properly_defined": false,
                    "issues": []
                }
            },
            "overall_coherence": {
                "score": 0,
                "details": {
                    "readability": "poor",
                    "complexity_level": "too_simple",
                    "issues": []
                }
            }
        },
        "total_score": 0,
        "improvement_suggestions": []
    }
    '''

def evaluate_use_case_diagram_with_llm(uml_code: str) -> Tuple[Dict, float]:
    """
    Enhanced evaluation of UML Use Case Diagram using detailed metrics and scoring.
    """
    # Create the evaluation criteria section
    evaluation_criteria = """
    1. Actor Analysis (1 point):
       - Count all unique actors (primary and secondary)
       - Verify actor naming conventions (should be roles, not specific people)
       - Check actor relationships (generalizations if any)
       - Award 1 point for correct actor implementation with proper naming
    
    2. Use Case Quality (1 point):
       - Count distinct use cases
       - Verify use case naming (verb phrases in active voice)
       - Check for appropriate abstraction level
       - Award 1 point for well-defined use cases following naming conventions
    
    3. Relationship Accuracy (1 point):
       - Count and classify all relationships:
         * Association relationships between actors and use cases
         * Include relationships between use cases
         * Extend relationships between use cases
         * Generalization relationships
       - Verify correct relationship direction and notation
       - Award 1 point for proper implementation of relationships
    
    4. System Boundary (1 point):
       - Verify system boundary definition
       - Check if all use cases are within boundary
       - Confirm actors are outside boundary
       - Award 1 point for correct system boundary implementation
    
    5. Overall Coherence (1 point):
       - Evaluate diagram complexity and readability
       - Check for balanced distribution of elements
       - Verify logical grouping of related use cases
       - Award 1 point for well-organized, readable diagram
    """

    # Get the evaluation template
    evaluation_template = get_evaluation_template()

    # Construct the prompt
    prompt = f"""You are a world-class UML expert specializing in Use Case diagram evaluation. 
    Your task is to perform a comprehensive analysis of the following Use Case Diagram using precise metrics and strict evaluation criteria.

    Analyze this PlantUML Use Case Diagram with extreme attention to detail:

    {uml_code}

    Evaluate the diagram based on these specific criteria and scoring guidelines:
    {evaluation_criteria}

    Provide your evaluation in the following JSON format. Fill in the appropriate values:
    {evaluation_template}

    Be extremely precise in your evaluation. Each metric must be thoroughly assessed with specific examples and clear justification for scores.
    """
    
    try:
        response = client.text_generation(prompt, max_new_tokens=10000, temperature=0.2)
        # Extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            evaluation = json.loads(json_match.group())
            return evaluation['metrics'], evaluation['total_score']
        else:
            return {"error": "Failed to parse evaluation"}, 0
    except Exception as e:
        print(f"Evaluation error: {str(e)}")
        return {"error": str(e)}, 0

def generate_optimal_use_case_uml(srs_text: str) -> str:
    """
    Enhanced generation of optimal UML Use Case diagram with detailed feedback loop.
    """
    iteration = 0
    max_iterations = 5
    optimal_score = 4.5
    best_uml_code = ""
    best_score = 0

    while iteration < max_iterations:
        iteration += 1
        
        # Basic template for UML generation
        uml_template = """
        @startuml
        left to right direction
        actor "Actor" as actor
        rectangle System {
            usecase "Use Case" as uc1
        }
        actor --> uc1
        @enduml
        """
        
        generation_prompt = f"""You are a senior UML architect specializing in Use Case diagrams. 
        Create a comprehensive Use Case diagram from this SRS document using PlantUML notation.
        
        Key Requirements:
        1. Identify all primary and secondary actors (use clear role names)
        2. Define precise use cases (use verb phrases)
        3. Implement appropriate relationships (association, include, extend, generalization)
        4. Define clear system boundary
        5. Ensure logical grouping and organization
        
        SRS Document:
        {srs_text}
        
        Follow these strict guidelines:
        - Use verb phrases for use cases (e.g., "Process Payment" not "Payment")
        - Actor names should reflect roles (e.g., "Bank Manager" not "John")
        - Include relationships must show mandatory inclusions
        - Extend relationships must show optional extensions
        - System boundary must be clearly defined
        - Group related use cases logically
        
        Base your response on this template structure but expand it according to the SRS:
        {uml_template}
        
        Generate the complete PlantUML code with precise formatting and comprehensive documentation.
        """
        
        response = client.text_generation(generation_prompt, max_new_tokens=1500, temperature=0.3)
        uml_code = extract_uml_code(response)
        
        # Evaluate the generated UML code
        metrics, score = evaluate_use_case_diagram_with_llm(uml_code)
        print(f"\nIteration {iteration} - Score: {score}/5")
        print("Metrics:", json.dumps(metrics, indent=2))
        
        if score > best_score:
            best_score = score
            best_uml_code = uml_code
            
        if score >= optimal_score:
            print("\nOptimal UML code generated!")
            return best_uml_code
            
        # Generate improvement feedback if not optimal
        if iteration < max_iterations:
            feedback_prompt = f"""You are a UML optimization expert. 
            The current UML diagram needs improvement.
            
            Current Diagram:
            {uml_code}
            
            Current Score: {score}/5
            
            Generate an improved version addressing these aspects:
            1. Actor clarity and relationships
            2. Use case precision and grouping
            3. Relationship accuracy and necessity
            4. System boundary definition
            5. Overall organization and readability
            
            Provide the improved PlantUML code with specific enhancements.
            """
            
            response = client.text_generation(feedback_prompt, max_new_tokens=1500, temperature=0.3)
            uml_code = extract_uml_code(response)

    print(f"\nMax iterations reached. Best score achieved: {best_score}/5")
    return best_uml_code

def extract_uml_code(response_text: str) -> str:
    """
    Enhanced extraction of UML code with validation.
    """
    try:
        start_idx = response_text.find("@startuml")
        end_idx = response_text.find("@enduml") + len("@enduml")
        
        if start_idx != -1 and end_idx != -1:
            uml_code = response_text[start_idx:end_idx].strip()
            # Validate basic UML structure
            if all(keyword in uml_code for keyword in ["@startuml", "@enduml"]):
                return uml_code
            else:
                return "Invalid UML code structure detected."
        else:
            return "No valid UML code found."
    except Exception as e:
        print(f"Error extracting UML code: {str(e)}")
        return "Error in UML code extraction."

def main():
    # Example usage
    pdf_path = "Automating-Software-Design-Process-using-LLM-s/library.pdf"
    srs_text = process_srs_document(pdf_path)
    
    if srs_text:
        uml_output = generate_optimal_use_case_uml(srs_text)
        
        # Save UML Code to File with timestamp
        if uml_output and "Invalid" not in uml_output and "Error" not in uml_output:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"optimal_use_case_uml_{timestamp}.txt"
            
            with open(filename, "w") as file:
                file.write(uml_output)
            print(f"\nUML code saved to {filename}")
        else:
            print("\nFailed to generate valid UML code.")
    else:
        print("\nFailed to process SRS document.")

if __name__ == "__main__":
    main()