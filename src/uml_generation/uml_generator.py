    
#Solving with the help of Hugging Face API Token
import re
import PyPDF2
from huggingface_hub import InferenceClient

# free Hugging Face API token
HUGGINGFACEHUB_API_TOKEN = "HUGGING_FACE_APIKEY"

# Initialize the Inference Client
client = InferenceClient(
    model="Qwen/Qwen2.5-Coder-32B-Instruct", 
    token=HUGGINGFACEHUB_API_TOKEN
)

# All Prompt Based Techinques

def construct_standard_cot_prompt_use_case(srs_text):
    """
    Construct a standard chain-of-thought prompt for generating a Use Case Diagram.
    """
    prompt = f'''
    You are an expert software designer. Analyze the following SRS document carefully.

    Step-by-step:
    1. Identify key actors mentioned explicitly or implied in the SRS (e.g., users, systems).
    2. Identify use cases based on functional requirements and relationships with actors.
    3. Specify how actors interact with each use case.

    Finally, generate a UML use case diagram in PlantUML format.

    SRS Document:
    {srs_text}

    Output:
    @startuml
    actor Actor1
    actor Actor2
    usecase "Use Case 1" as UC1
    usecase "Use Case 2" as UC2
    Actor1 --> UC1
    Actor2 --> UC2
    @enduml
    '''
    return prompt
def construct_standard_cot_prompt_activity(srs_text):
    """
    Construct a standard chain-of-thought prompt for generating an Activity Diagram.
    """
    prompt = f'''
    You are an expert software designer. Analyze the following SRS document carefully.

    Step-by-step:
    1. Identify the main activities and decisions described in the SRS.
    2. Determine the flow of these activities, including start and end points.
    3. Map out these activities and decisions in a sequential order.

    Finally, generate a UML activity diagram in PlantUML format.

    SRS Document:
    {srs_text}

    Output:
    @startuml
    start
    :Activity 1;
    if (Decision?) then (yes)
      :Activity 2;
    else (no)
      :Activity 3;
    endif
    stop
    @enduml
    '''
    return prompt
def construct_standard_cot_prompt_class(srs_text):
    """
    Construct a standard chain-of-thought prompt for generating a Class Diagram.
    """
    prompt = f'''
    You are an expert software designer. Analyze the following SRS document carefully.

    Step-by-step:
    1. Identify the main classes and their responsibilities described in the SRS.
    2. Determine the attributes and methods for each class.
    3. Identify relationships between classes (e.g., inheritance, association).

    Finally, generate a UML class diagram in PlantUML format.

    SRS Document:
    {srs_text}

    Output:
    @startuml
    class Class1 {{
      +Attribute1: Type
      +Method1(): ReturnType
    }}
    class Class2 {{
      +Attribute2: Type
      +Method2(): ReturnType
    }}
    Class1 --> Class2 : Relationship
    @enduml
    '''
    return prompt


#Few Shot Promting


def construct_few_shot_cot_prompt_use_case(srs_text):
    """
    Construct a few-shot chain-of-thought prompt for generating a Use Case Diagram.
    """
    example_1 = '''
    SRS Document:
    A system for managing appointments and medical records. Key features include:
    - Patients book, update, or cancel appointments.
    - Doctors review medical records.
    - Admins manage patient information.

    Step-by-step:
    1. Actors: Patient, Doctor, Admin
    2. Use Cases: "Book Appointment", "Review Medical Records", "Manage Patient Info"
    3. Relationships:
       - Patient --> "Book Appointment"
       - Doctor --> "Review Medical Records"
       - Admin --> "Manage Patient Info"

    Output:
    @startuml
    actor Patient
    actor Doctor
    actor Admin
    usecase "Book Appointment" as UC1
    usecase "Review Medical Records" as UC2
    usecase "Manage Patient Info" as UC3
    Patient --> UC1
    Doctor --> UC2
    Admin --> UC3
    @enduml
    '''
    
    prompt = f'''
    {example_1}
    
    SRS Document:
    {srs_text}

    Step-by-step:
    1. (Identify Actors)
    2. (Identify Use Cases)
    3. (Define Relationships)
    
    Output:
    @startuml
    (Actors, Use Cases, Relationships)
    @enduml
    '''
    return prompt
def construct_few_shot_cot_prompt_activity(srs_text):
    """
    Construct a few-shot chain-of-thought prompt for generating an Activity Diagram.
    """
    example_1 = '''
    SRS Document:
    A system for processing online orders. Key features include:
    - Customer places an order.
    - System processes payment.
    - Warehouse prepares shipment.
    - Delivery service ships the order.

    Step-by-step:
    1. Identify main activities: Place Order, Process Payment, Prepare Shipment, Ship Order
    2. Determine decision points: Payment successful?
    3. Map the flow of activities and decisions.

    Output:
    @startuml
    start
    :Place Order;
    :Process Payment;
    if (Payment successful?) then (yes)
      :Prepare Shipment;
      :Ship Order;
    else (no)
      :Cancel Order;
    endif
    stop
    @enduml
    '''
    
    prompt = f'''
            {example_1}
            
            SRS Document:
            {srs_text}

            Step-by-step:
            1. (Identify Activities)
            2. (Identify Decisions)
            3. (Map Flow)
            
            Output:
            @startuml
            (Activities, Decisions, Flow)
            @enduml
            '''
    return prompt
def construct_few_shot_cot_prompt_class(srs_text):
    """
    Construct a few-shot chain-of-thought prompt for generating a Class Diagram.
    """
    example_1 = '''
                    SRS Document:
                    A library management system. Key features include:
                    - Books have titles, authors, and ISBNs.
                    - Members can borrow books.
                    - Librarians manage book inventory.

                    Step-by-step:
                    1. Identify main classes:
                    - Book
                    - Member
                    - Librarian
                    2. Determine attributes and methods for each class:
                    - Book: title, author, ISBN; Methods: getDetails()
                    - Member: name, memberID; Methods: borrowBook()
                    - Librarian: employeeID; Methods: addBook(), removeBook()
                    3. Identify relationships:
                    - A Member can borrow multiple Books.
                    - A Librarian manages Books.

                    Output:
                    @startuml
                    class Book {
                    -title: String
                    -author: String
                    -ISBN: String
                    +getDetails(): String
                    }
                    class Member {
                    -name: String
                    -memberID: Integer
                    +borrowBook(): void
                    }
                    class Librarian {
                    -employeeID: Integer
                    +addBook(): void
                    +removeBook(): void
                    }
                    Member --> Book : borrows
                    Librarian --> Book : manages
                    @enduml
                    '''
    
    prompt = f'''
                {example_1}
                
                SRS Document:
                {srs_text}

                Step-by-step:
                1. Identify the main classes described in the SRS.
                2. Determine attributes and methods for each class.
                3. Identify relationships between the classes.

                Output:
                @startuml
                (Classes, Attributes, Methods, Relationships)
                @enduml
                '''
    return prompt


#Role play Prompting

def role_play_prompt_use_case(srs_text):
    """
    Role Play Prompt for generating UML Use Case Diagrams.
    """
    prompt = f"""
    You are a UML expert specializing in Use Case Diagrams. Your task is to analyze the provided SRS document
    and generate a UML Use Case Diagram in PlantUML syntax.

    Responsibilities:
    1. Identify actors (e.g., users, external systems) explicitly or implicitly mentioned in the SRS.
    2. Identify use cases based on functional requirements.
    3. Map relationships between actors and use cases.

    Guidelines:
    - Use PlantUML syntax for the output.
    - Only output the UML diagram; avoid additional explanations.

    Example syntax:
    @startuml
    actor Actor1
    actor Actor2
    usecase "Use Case 1" as UC1
    usecase "Use Case 2" as UC2
    Actor1 --> UC1
    Actor2 --> UC2
    @enduml

    SRS Document:
    {srs_text}

    Generate the UML Use Case Diagram below:
    """
    return prompt
def role_play_prompt_activity(srs_text):
    """
    Role Play Prompt for generating UML Activity Diagrams.
    """
    prompt = f"""
    You are a UML expert specializing in Activity Diagrams. Your task is to analyze the provided SRS document
    and generate a UML Activity Diagram in PlantUML syntax.

    Responsibilities:
    1. Identify activities and processes described in the SRS.
    2. Map the sequence of activities, including any decision points or conditions.
    3. Use PlantUML Activity Diagram syntax for the output.

    Guidelines:
    - Include start and stop points.
    - Clearly define transitions between activities.
    - Use decision nodes for branching.

    Example syntax:
    @startuml
    start
    :Activity 1;
    if (Condition?) then (yes)
      :Activity 2;
    else (no)
      :Activity 3;
    endif
    stop
    @enduml

    SRS Document:
    {srs_text}

    Generate the UML Activity Diagram below:
    """
    return prompt
def role_play_prompt_class(srs_text):
    """
    Role Play Prompt for generating UML Class Diagrams.
    """
    prompt = f"""
    You are a UML expert specializing in Class Diagrams. Your task is to analyze the provided SRS document
    and generate a UML Class Diagram in PlantUML syntax.

    Responsibilities:
    1. Identify main classes and their responsibilities described in the SRS.
    2. Define attributes and methods for each class.
    3. Identify relationships between classes (e.g., inheritance, association, dependency).

    Guidelines:
    - Use PlantUML syntax for the output.
    - Clearly define attributes, methods, and relationships.

    Example syntax:
    @startuml
    class Class1 {{
      -attribute1: Type
      +method1(): ReturnType
    }}
    class Class2 {{
      +attribute2: Type
      +method2(): ReturnType
    }}
    Class1 --> Class2 : RelationshipType
    @enduml

    SRS Document:
    {srs_text}

    Generate the UML Class Diagram below:
    """
    return prompt


# level Based Prompting for use case

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
    response = client.text_generation(prompt, max_new_tokens=10000, temperature=0.2)
    return response.strip()
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
    response = client.text_generation(prompt, max_new_tokens=10000, temperature=0.2)
    return response.strip()
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
    response = client.text_generation(prompt,max_new_tokens=10000, temperature=0.2)
    return response.strip()
def level_4_generate_uml(actors, use_cases, relationships):
    prompt = f"""
    Generate a detailed UML Use Case Diagram in PlantUML syntax based on the provided actors, use cases, and relationships.
    Ensure the following:
    1. The output begins with "@startuml" and ends with "@enduml".
    2. Do not include any extraneous occurrences of "@startuml" or "@enduml" in the middle of the output.
    3. Format the diagram with clear and concise syntax.

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
    response = client.text_generation(prompt, max_new_tokens=15000, temperature=0.2)
    
    return response.strip()
def generate_uml_code(srs_text):
    try:
        # Level 1: Identify Actors
        actors = level_1_actors(srs_text)
        # print("Level 1 - Actors Identified:", actors)

        # Level 2: Identify Use Cases
        use_cases = level_2_use_cases(srs_text, actors)
        # print("Level 2 - Use Cases Identified:", use_cases)

        # Level 3: Establish Relationships
        relationships = level_3_relationships(actors, use_cases)
        # print("Level 3 - Relationships Established:", relationships)

        # Level 4: Generate UML Code
        uml_code = level_4_generate_uml(actors, use_cases, relationships)
        # print("Level 4 - UML Code Generated:\n", uml_code)

        # optimal_use_case_uml = generate_optimal_uml(
        #                             res=uml_code,
        #                             evaluate_uml_with_llm=evaluate_use_case_diagram_with_llm,
        #                             diagram_type="Use Case Diagram"
        #                         )

        # metrics,score,ju = evaluate_use_case_diagram_with_llm(uml_code)
        # print("Metrics For evalution of Use Case is ",metrics)
        # print("score:",score)
        # print("justification",ju)
        # Extract PlantUML code only
        # print(uml_code)
        # return uml_code
        return extract_uml_code(uml_code)
    except Exception as e:
        print("Error during UML generation:", e)
        return None

#levels for class diagram 
def level_1_classes(srs_text):
    prompt = f"""
    Analyze the following SRS document to identify the main classes (both explicit and implicit) described.
    List them step-by-step, focusing on the entities or abstractions mentioned in the document.

    SRS Document:
    {srs_text}

    Output:
    Classes:
    1. (Class 1)
    2. (Class 2)
    """
    response = client.text_generation(prompt, max_new_tokens=5000, temperature=0.2)
    return response.strip()
def level_2_attributes_methods(srs_text, classes):
    prompt = f"""
    Based on the following SRS document and identified classes, extract the attributes and methods for each class.
    List them step-by-step for each class.

    SRS Document:
    {srs_text}

    Identified Classes:
    {classes}

    Output:
    Class 1:
      - Attributes:
        1. (Attribute 1)
        2. (Attribute 2)
      - Methods:
        1. (Method 1)
        2. (Method 2)

    Class 2:
      - Attributes:
        ...
      - Methods:
        ...
    """
    response = client.text_generation(prompt, max_new_tokens=5000, temperature=0.2)
    return response.strip()
def level_3_class_relationships(classes, attributes_methods):
    prompt = f"""
    Based on the identified classes, attributes, and methods, determine the relationships between the classes.
    Specify the type of relationships (e.g., association, inheritance, dependency) and their direction.

    Classes:
    {classes}

    Attributes and Methods:
    {attributes_methods}

    Output:
    Relationships:
    Class1 --> Class2 : Inheritance
    Class1 -- Class3 : Association
    """
    response = client.text_generation(prompt, max_new_tokens=5000, temperature=0.2)
    return response.strip()
def level_4_generate_class_uml(classes, attributes_methods, relationships):
    
    prompt = f"""
    Generate a detailed UML Class Diagram in PlantUML syntax based on the identified classes, attributes, methods, and relationships.

    Classes:
    {classes}

    Attributes and Methods:
    {attributes_methods}

    Relationships:
    {relationships}

    Output:
    @startuml
    class Class1 {{
      + Attribute1
      - Method1()
    }}
    Class1 --> Class2 : Inheritance
    @enduml
    """
    response = client.text_generation(prompt, max_new_tokens=10000, temperature=0.2)
    return response.strip()
def generate_class_diagram_code(srs_text):
    try:
        # Level 1: Identify Classes
        classes = level_1_classes(srs_text)
        # print("Level 1 - Classes Identified:", classes)

        # Level 2: Identify Attributes and Methods
        attributes_methods = level_2_attributes_methods(srs_text, classes)
        # print("Level 2 - Attributes and Methods Identified:", attributes_methods)

        # Level 3: Define Relationships
        relationships = level_3_class_relationships(classes, attributes_methods)
        # print("Level 3 - Relationships Defined:", relationships)

        # Level 4: Generate UML Code
        uml_code = level_4_generate_class_uml(classes, attributes_methods, relationships)
        # print("Level 4 - UML Code Generated:\n", uml_code)

  #       optimal_class_uml = generate_optimal_uml(
  #                           res=uml_code,
  #                           evaluate_uml_with_llm=evaluate_class_diagram_with_llm,
  #                           diagram_type="Class Diagram"
  #                       )
  # # Reusing the optimization function
  #       return optimal_class_uml
        return extract_uml_code(uml_code)
    except Exception as e:
        print("Error during Class Diagram UML generation:", e)
        return None


#levels for acitivity diagram
def level_1_activities(srs_text):
    prompt = f"""
    Analyze the following SRS document to identify the main activities or actions described.
    List them step-by-step in a simple format.

    SRS Document:
    {srs_text}

    Output:
    Activities:
    1. (Activity 1)
    2. (Activity 2)
    """
    response = client.text_generation(prompt, max_new_tokens=5000, temperature=0.2)
    return response.strip()
def level_2_transitions(srs_text, activities):
    prompt = f"""
    Based on the following SRS document and identified activities, list the transitions between activities.
    Include conditional and parallel flows if mentioned.

    SRS Document:
    {srs_text}

    Identified Activities:
    {activities}

    Output:
    Transitions:
    Activity1 --> Activity2 : (Condition/Trigger)
    Activity2 --> Activity3 : (Condition/Trigger)
    """
    response = client.text_generation(prompt, max_new_tokens=5000, temperature=0.2)
    return response.strip()
def level_3_control_flow(activities, transitions):
    prompt = f"""
    Based on the identified activities and their transitions, define the control flow.
    Specify branching points, loops, and parallel paths.

    Activities:
    {activities}

    Transitions:
    {transitions}

    Output:
    Control Flow:
    1. Activity1 -> Activity2
    2. Activity2 -> Activity3 [Condition]
    3. Parallel:
       - Activity3 -> Activity4
       - Activity3 -> Activity5
    """
    response = client.text_generation(prompt, max_new_tokens=5000, temperature=0.2)
    return response.strip()
def level_4_generate_activity_uml(activities, transitions, control_flow):
    prompt = f"""
    Generate a detailed UML Activity Diagram in PlantUML syntax based on the identified activities, transitions, and control flow.

    Activities:
    {activities}

    Transitions:
    {transitions}

    Control Flow:
    {control_flow}

    Output:
    @startuml
    start
    :Activity1;
    :Activity2;
    if (Condition?) then (yes)
      :Activity3;
    else (no)
      :Activity4;
    endif
    stop
    @enduml
    """
    response = client.text_generation(prompt, max_new_tokens=5000, temperature=0.2)
    return response.strip()
def generate_activity_diagram_code(srs_text):
    try:
        # Level 1: Identify Activities
        activities = level_1_activities(srs_text)
        # print("Level 1 - Activities Identified:", activities)

        # Level 2: Identify Transitions
        transitions = level_2_transitions(srs_text, activities)
        # print("Level 2 - Transitions Identified:", transitions)

        # Level 3: Define Control Flow
        control_flow = level_3_control_flow(activities, transitions)
        # print("Level 3 - Control Flow Defined:", control_flow)

        # Level 4: Generate UML Code
        uml_code = level_4_generate_activity_uml(activities, transitions, control_flow)
        # print("Level 4 - UML Code Generated:\n", uml_code)

        # optimal_activity_uml = generate_optimal_uml(
        #                 res=uml_code,
        #                 evaluate_uml_with_llm=evaluate_activity_diagram_with_llm,
        #                 diagram_type="Activity Diagram"
        #             )
        # # Reusing the optimization function
        # return optimal_activity_uml
        return extract_uml_code(uml_code)
    except Exception as e:
        print("Error during Activity Diagram UML generation:", e)
        return None


# def evaluate_use_case_diagram_with_llm(uml_code):
#     """
#     Evaluate the UML Use Case Diagram using an LLM with enhanced scoring and metrics evaluation.
#     """
#     prompt = f"""
#     You are an expert in evaluating UML diagrams. Analyze the following Use Case Diagram in PlantUML format
#     and evaluate it based on the following metrics and scoring rules:

#     1. Number of Actors (NA):
#        - Ideal Range: 2-7.
#        - Scoring:
#          - 2-7 actors: +1 point.
#          - 1 actor: 0 points.
#          - >7 actors: +0.5 point.

#     2. Number of Use Cases (NUC):
#        - Ideal Range: 5-15.
#        - Scoring:
#          - 5-15 use cases: +1 point.
#          - <5 use cases: +0.5 point.
#          - >15 use cases: +0.5 point.

#     3. Actor-to-Use Case Ratio (AUC):
#        - Ideal Ratio: Between 1:3 and 1:7.
#        - Scoring:
#          - 1:3 to 1:7: +1 point.
#          - <1:3: +0.5 point.
#          - >1:7: +0.5 point.

#     4. Relationships (Include/Extend):
#        - Ideal Range: 10-20 relationships.
#        - Scoring:
#          - 10-20 relationships: +1 point.
#          - <10 relationships: +0.5 point.
#          - >20 relationships: +0.5 point.

#     Diagram:
#     {uml_code}

#     Based on these rules, provide the evaluation in the following format:
#     Metrics:
#     - Number of Actors (NA): <value> (Score: <score>)
#     - Number of Use Cases (NUC): <value> (Score: <score>)
#     - Actor-to-Use Case Ratio (AUC): <value> (Score: <score>)
#     - Relationships (Include/Extend): <value> (Score: <score>)

#     Total Score: <value out of 5>
#     """
    
#     response = client.text_generation(prompt, max_new_tokens=10000, temperature=0.2)

#     # Extract metrics and score using regex
#     metrics_match = re.search(r"Metrics:\s*([\s\S]*?)Total Score:", response)
#     score_match = re.search(r"Total Score:\s*(\d+(\.\d+)?)", response)

#     if metrics_match and score_match:
#         metrics_text = metrics_match.group(1).strip()
#         score = float(score_match.group(1))
#         return metrics_text, score
#     else:
#         return "Evaluation failed", 0



def evaluate_use_case_diagram_with_llm(uml_code):
    """
    Evaluate the UML Use Case Diagram using an LLM with combined metrics and scoring logic.
    """
    prompt = f"""
    You are an expert in evaluating UML diagrams. Analyze the following Use Case Diagram in PlantUML format
    and evaluate it based on these metrics and norms:

    Metrics for Evaluation:
    1. Correctness:
       - Checks the accuracy of actors, use cases, and relationships.
       - Scoring:
         - Perfect alignment with requirements: +2 points.
         - Minor omissions or errors: +1 point.
         - Significant omissions or errors: 0 points.

    2. Completeness:
       - Assesses whether the diagram covers all key requirements.
       - Scoring:
         - Covers all critical requirements: +2 points.
         - Covers most (75% or more): +1 point.
         - Covers less than 75%: 0 points.

    3. Terminological Alignment:
       - Evaluates consistency in terminology between the diagram and requirements.
       - Scoring:
         - Fully consistent: +2 points.
         - Minor inconsistencies: +1 point.
         - Major inconsistencies: 0 points.

    4. Understandability:
       - Rates the clarity and absence of redundancies in the diagram.
       - Scoring:
         - Clear, well-structured: +2 points.
         - Some ambiguities or redundancies: +1 point.
         - Confusing or unclear: 0 points.

    5. Complexity:
       - Evaluates the balance between actors, use cases, and relationships.
       - Ideal ranges:
         - Actors: 2-7
         - Use Cases: 5-15
         - Relationships (Include/Extend): 10-20
       - Scoring:
         - Balanced complexity: +2 points.
         - Slightly unbalanced: +1 point.
         - Overly simple or overly complex: 0 points.

    6. Adherence to Standards:
       - Ensures the diagram adheres to UML syntax and semantics.
       - Scoring:
         - Fully adheres to standards: +2 points.
         - Minor deviations: +1 point.
         - Major errors: 0 points.

    Additional Metrics for Evaluation:
    7. Number of Actors (NA):
       - Description: Counts how many distinct actors are represented.
       - Scoring:
         - Ideal range (2-7 actors): +2 points.
         - Too few or too many actors: +1 point.
         - Extremely unbalanced: 0 points.
       - Rationale: A large number of actors may indicate complexity but 
        can also reduce understandability.

    8. Number of Use Cases (NUC):
       - Description: Total count of use cases in the diagram.
       - Scoring:
         - Ideal range (5-15 use cases): +2 points.
         - Slightly more or fewer: +1 point.
         - Significantly unbalanced: 0 points.
       - Rationale: Too many use cases might suggest the need for modularization.

    9. Actor-to-Use Case Ratio (AUC):
       - Description: Ratio of the number of actors to the number of use cases.
       - Scoring:
         - Ideal range (1:3 to 1:7): +2 points.
         - Slightly unbalanced: +1 point.
         - Significantly unbalanced: 0 points.
       - Rationale: Helps assess whether actor responsibilities are evenly distributed.

    10. Relationships Between Use Cases:
        - Description: Counts the number of include and extend relationships.
        - Scoring:
          - Ideal range (10-20 relationships): +2 points.
          - Slightly fewer or more: +1 point.
          - Extremely unbalanced: 0 points.
        - Rationale: Proper use of relationships can promote modularization and reuse.

    Diagram:
    {uml_code}

    Evaluation Format:
    Metrics:
    - Correctness: <score> (Reason: <explanation>)
    - Completeness: <score> (Reason: <explanation>)
    - Terminological Alignment: <score> (Reason: <explanation>)
    - Understandability: <score> (Reason: <explanation>)
    - Complexity: <score> (Reason: <explanation>)
    - Adherence to Standards: <score> (Reason: <explanation>)
    - Number of Actors (NA): <score> (Reason: <explanation>)
    - Number of Use Cases (NUC): <score> (Reason: <explanation>)
    - Actor-to-Use Case Ratio (AUC): <score> (Reason: <explanation>)
    - Relationships Between Use Cases: <score> (Reason: <explanation>)

    Total Score: <score out of 20>
    Justification:
    <Detailed explanation of observed issues, strengths, and weaknesses across metrics.>
    """

    # Call LLM for response
    response = client.text_generation(prompt, max_new_tokens=20000, temperature=0.2)

    # Extract metrics, total score, and justification from response
    metrics_match = re.search(r"Metrics:\s*([\s\S]*?)Total Score:", response)
    score_match = re.search(r"Total Score:\s*(\d+(\.\d+)?)", response)
    justification_match = re.search(r"Justification:\s*([\s\S]*)", response)

    if metrics_match and score_match and justification_match:
        metrics_text = metrics_match.group(1).strip()
        score = float(score_match.group(1))
        justification = justification_match.group(1).strip()
        return metrics_text, score, justification
    else:
        return "Evaluation failed", 0, "No justification provided."
# Class Diagram Metrics Evaluation
def evaluate_class_diagram_with_llm(uml_code):
    """
    Evaluate the UML Class Diagram using an LLM.
    """
    prompt = f"""
    You are an expert in evaluating UML diagrams. Analyze the following Class Diagram in PlantUML format
    and evaluate it based on the following metrics:

    1. Number of Classes (NC): Count the number of distinct classes.
    2. Depth of Inheritance Tree (DIT): Determine the maximum length from the root to the leaf in the inheritance hierarchy.
    3. Number of Children (NOC): Count the number of immediate subclasses for each class.
    4. Coupling Between Objects (CBO): Count the number of classes each class is coupled to.
    5. Lack of Cohesion in Methods (LCOM): Assess class cohesion based on relatedness of methods.
    6. Weighted Methods per Class (WMC): Sum of complexity weights for all methods in a class.

    Diagram:
    {uml_code}

    Provide your evaluation in the following format:
    Metrics:
    - Number of Classes (NC): <value>
    - Depth of Inheritance Tree (DIT): <value>
    - Number of Children (NOC): <value>
    - Coupling Between Objects (CBO): <value>
    - Lack of Cohesion in Methods (LCOM): <value>
    - Weighted Methods per Class (WMC): <value>

    Score:
    <value out of 5>
    """
    response = client.text_generation(prompt, max_new_tokens=500, temperature=0.2)
    metrics_match = re.search(r"Metrics:\s*([\s\S]*?)Score:", response)
    score_match = re.search(r"Score:\s*(\d+)", response)

    if metrics_match and score_match:
        metrics_text = metrics_match.group(1).strip()
        score = int(score_match.group(1))
        return metrics_text, score
    else:
        return "Evaluation failed", 0
 
# Activity Diagram Metrics Evaluation
def evaluate_activity_diagram_with_llm(uml_code):
    """
    Evaluate the UML Activity Diagram using an LLM.
    """
    prompt = f"""
    You are an expert in evaluating UML diagrams. Analyze the following Activity Diagram in PlantUML format
    and evaluate it based on the following metrics:

    1. Number of Activities (NOA): Count the total number of activities.
    2. Number of Transitions (NOT): Count the number of transitions between activities.
    3. Control Flow Complexity (CFC): Assess decision points and branching complexity.
    4. Parallel Complexity (Fork-Join Complexity): Evaluate the number of parallel paths.

    Diagram:
    {uml_code}

    Provide your evaluation in the following format:
    Metrics:
    - Number of Activities (NOA): <value>
    - Number of Transitions (NOT): <value>
    - Control Flow Complexity (CFC): <value>
    - Parallel Complexity (Fork-Join Complexity): <value>

    Score:
    <value out of 5>
    """
    response = client.text_generation(prompt, max_new_tokens=500, temperature=0.2)
    metrics_match = re.search(r"Metrics:\s*([\s\S]*?)Score:", response)
    score_match = re.search(r"Score:\s*(\d+)", response)

    if metrics_match and score_match:
        metrics_text = metrics_match.group(1).strip()
        score = int(score_match.group(1))
        return metrics_text, score
    else:
        return "Evaluation failed", 0

    
    
    
def generate_optimal_uml(res, evaluate_uml_with_llm, diagram_type="UML Diagram"):
    """
    Generalized function to iteratively refine and generate optimal UML diagrams with clarity, modularity, and correct syntax.

    Parameters:
    - res: Initial generated UML code.
    - evaluate_uml_with_llm: Evaluation function for the diagram type.
    - diagram_type: Type of the diagram (e.g., "Use Case Diagram", "Class Diagram").

    Returns:
    - Refined UML code.
    """
    iteration = 0
    max_iterations = 2
    optimal_score = 4  # Define the desired score threshold
    previous_uml_code = None  # Track previous UML code to ensure progress

    while iteration < max_iterations:
        iteration += 1
        uml_code = extract_uml_code(res)
        print(f"Iteration {iteration} - Current UML Code:\n{uml_code}")

        # Evaluate the generated UML code using the specified evaluation function
        metrics, score = evaluate_uml_with_llm(uml_code)
        print(f"Iteration {iteration} - Score: {score}")
        print("Metrics:", metrics)

        # Check if the score meets the optimal threshold
        if score >= optimal_score:
            print(f"Optimal {diagram_type} generated.")
            return uml_code

        # Compare with the previous UML code
        if uml_code == previous_uml_code:
            print("No progress detected. Modifying feedback prompt for better refinement.")
            additional_feedback = (
                "Ensure the syntax is correct and includes '@startuml' at the beginning and '@enduml' at the end. "
                "Remove any extraneous syntax or elements."
            )
        else:
            additional_feedback = "Ensure syntax correctness while improving clarity and structure."

        # Provide feedback and iterate
        feedback_prompt = f"""
        The following {diagram_type} was generated:
        {uml_code}

        The evaluation metrics are as follows:
        {metrics}

        The score is {score}, which is below the desired threshold of {optimal_score}.
        Please refine the diagram with the following rules:
        - Ensure the syntax is PlantUML compliant with '@startuml' at the beginning and '@enduml' at the end.
        - Verify that all actors, use cases, and relationships are properly defined and formatted.
        - Simplify relationships to avoid clutter.
        - Break the diagram into smaller, modular components where possible.
        - Group related elements for better readability.
        - Reduce excessive connections and focus on the most critical elements.
        - Be syntactically correct for syntax use existing syntax
        - use Package Syntax for grouping in uml code use that 
        - {additional_feedback}

        Generate a revised {diagram_type} with correct syntax.
        """
        response = client.text_generation(feedback_prompt, max_new_tokens=15000, temperature=0.2)
        previous_uml_code = uml_code  # Update the previous UML code for comparison
        res = response  # Use the response as input for the next iteration

    print(f"Max iterations reached. Returning the best attempt for {diagram_type}.")
    return uml_code



def extract_uml_code(response_text):
    """
    Extract and return only the UML code from the response.
    """
    start_idx = response_text.find("@startuml")
    end_idx = response_text.find("@enduml") + len("@enduml")
    
    if start_idx != -1 and end_idx != -1:
        return response_text[start_idx:end_idx].strip()
    else:
        return "No valid UML code found."


# Use Case Diagram Metrics Evaluation

# def evaluate_use_case_diagram_with_llm(uml_code):
#     """
#     Evaluate the UML Use Case Diagram using an LLM.
#     """
#     prompt = f"""
#     You are an expert in evaluating UML diagrams. Analyze the following Use Case Diagram in PlantUML format
#     and evaluate it based on the following metrics:

#     1. Number of Actors (NA): Count the number of distinct actors.
#     2. Number of Use Cases (NUC): Count the number of distinct use cases.
#     3. Actor-to-Use Case Ratio (AUC): Compute the ratio of actors to use cases.
#     4. Relationships (Include/Extend): Count the number of relationships (arrows) in the diagram.

#     Diagram:
#     {uml_code}

#     Provide your evaluation in the following format:
#     Metrics:
#     - Number of Actors (NA): <value>
#     - Number of Use Cases (NUC): <value>
#     - Actor-to-Use Case Ratio (AUC): <value>
#     - Relationships (Include/Extend): <value>

#     Score:
#     <value out of 5>
#     """
    
#     response = client.text_generation(prompt, max_new_tokens=10000, temperature=0.2)

#     # Extract metrics and score using regex
#     metrics_match = re.search(r"Metrics:\s*([\s\S]*?)Score:", response)
#     score_match = re.search(r"Score:\s*(\d+)", response)

#     if metrics_match and score_match:
#         metrics_text = metrics_match.group(1).strip()
#         score = int(score_match.group(1))
#         return metrics_text, score
#     else:
#         return "Evaluation failed", 0

# Feedback Loop for Generating Optimal UML Code
# def generate_optimal_use_case_uml(res):
    # iteration = 0
    # max_iterations = 5
    # optimal_score = 4  # Define the desired score threshold

    # while iteration < max_iterations:
    #     iteration += 1
    #     uml_code = extract_uml_code(res)

    #     # Evaluate the generated UML code using LLM
    #     metrics, score = evaluate_use_case_diagram_with_llm(uml_code)
    #     print(f"Iteration {iteration} - Score: {score}")
    #     print("Metrics:", metrics)

    #     # If score meets the optimal threshold, return the UML code
    #     if score >= optimal_score:
    #         print("Optimal UML code generated.")
    #         return uml_code

    #     # Provide feedback and iterate
    #     feedback_prompt = f"""
    #     The following UML Use Case Diagram was generated:
    #     {uml_code}

    #     The evaluation metrics are as follows:
    #     {metrics}

    #     The score is {score}, which is below the desired threshold of {optimal_score}.
    #     Please refine the diagram by:
    #     - Ensuring all actors and use cases are properly defined.
    #     - Adding missing relationships or refining existing ones.

    #     Generate a revised UML Use Case Diagram.
    #     """
    #     response = client.text_generation(feedback_prompt, max_new_tokens=1000, temperature=0.7)
    #     uml_code = extract_uml_code(response)

    # print("Max iterations reached. Returning the best attempt.")
    # return uml_code

# def generate_optimal_uml(res, evaluate_uml_with_llm, diagram_type="UML Diagram"):
#     """
#     Generalized function to iteratively refine and generate optimal UML diagrams.
    
#     Parameters:
#     - res: Initial generated UML code.
#     - evaluate_uml_with_llm: Evaluation function for the diagram type.
#     - diagram_type: Type of the diagram (e.g., "Use Case Diagram", "Class Diagram").

#     Returns:
#     - Refined UML code.
#     """
#     iteration = 0
#     max_iterations = 3
#     optimal_score = 4  # Define the desired score threshold

#     while iteration < max_iterations:
#         iteration += 1
#         uml_code = extract_uml_code(res)
#         # print("this is the uml code",res)

#         # Evaluate the generated UML code using the specified evaluation function
#         metrics, score = evaluate_uml_with_llm(uml_code)
#         print(f"Iteration {iteration} - Score: {score}")
#         print("Metrics:", metrics)

#         # If score meets the optimal threshold, return the UML code
#         if score >= optimal_score:
#             print(f"Optimal {diagram_type} generated.")
#             return uml_code

#         # Provide feedback and iterate
#         feedback_prompt = f"""
#         The following {diagram_type} was generated:
#         {uml_code}

#         The evaluation metrics are as follows:
#         {metrics}

#         The score is {score}, which is below the desired threshold of {optimal_score}.
#         Please refine the diagram by:
#         - Ensuring all elements are properly defined.
#         - Adding missing relationships or refining existing ones.
#         - Improving clarity or modularization where applicable.

#         Generate a revised {diagram_type}.
#         """
#         response = client.text_generation(feedback_prompt, max_new_tokens=15000, temperature=0.2)
#         # print("This is ouput ",response)
#         uml_code = extract_uml_code(response)
        

#     print(f"Max iterations reached. Returning the best attempt for {diagram_type}.")
#     return uml_code





# older uml code


# def generate_uml_code(srs_text):

#     "Process the PDF, construct the prompt, and get UML code using the LLM."


#     # Construct the prompt
#     prompt = construct_standard_cot_prompt_use_case(srs_text)
    
#     # Call the LLM
#     try:
#         response = client.text_generation(
#             prompt,
#             max_new_tokens=10000,  # Adjust token limit based on your requirements
#             temperature=0.7
#         )
#         uml_code = extract_uml_code(response)  # Extract PlantUML code only
#         print(uml_code)
#         return uml_code
#     except Exception as e:
#         print("Error during UML generation:", e)
#         return None


# # Example usage
# import PyPDF2
# def process_srs_document(pdf_path):
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
#     return text

# pdf_path = "Automating-Software-Design-Process-using-LLM-s/src/uml_generation/inventory.pdf"
# out = process_srs_document(pdf_path)
# uml_code = generate_uml_code(out)

# if uml_code:
#     with open("uml_output.txt", "w") as output_file:
#         output_file.write(uml_code)
#     print("UML code saved to uml_output.txt")


# test_srs = "The system has two actors: Admin and User. Admin can approve requests. User can submit requests."
# actors = level_1_actors(test_srs)
# use_cases = level_2_use_cases(test_srs, actors)
# relationships = level_3_relationships(actors, use_cases)
# uml_code = level_4_generate_uml(actors, use_cases, relationships)
# print(uml_code)
