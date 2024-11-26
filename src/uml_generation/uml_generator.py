
#Traditional Apparoch Consiting of Using NLP Techniques to Extract the Information
'''
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2"  
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

import PyPDF2
def process_srs_document(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def generate_use_case_uml(processed_data):
    entities = processed_data.get('entities', [])
    noun_phrases = processed_data.get('noun_phrases', [])
    
    actors = list(set([ent[0] for ent in entities if ent[1] in ['PERSON', 'ORG']]))[:5]  
    use_cases = list(set([np for np in noun_phrases if np.lower().startswith(('manage', 'create', 'update', 'delete', 'view', 'process', 'generate', 'analyze'))][:10]))  # Limit to 10 use cases
    
    uml_code = "@startuml\n"
    
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



__all__ = ['generate_uml_code']    

'''


    
#Solving with the help of Hugging Face API Token

import PyPDF2
from huggingface_hub import InferenceClient

# free Hugging Face API token
HUGGINGFACEHUB_API_TOKEN = "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"

# Initialize the Inference Client
client = InferenceClient(
    model="Qwen/Qwen2.5-Coder-32B-Instruct", 
    token=HUGGINGFACEHUB_API_TOKEN
)

#Standard Chain of though USE CASE Diagram
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

#Standard Chain of though Activiy Diagram
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

#Class diagram
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


def generate_uml_code(srs_text):
    """
    Process the PDF, construct the prompt, and get UML code using the LLM.
    """

    # Construct the prompt
    prompt = construct_standard_cot_prompt_use_case(srs_text)
    
    # Call the LLM
    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=10000,  # Adjust token limit based on your requirements
            temperature=0.7
        )
        uml_code = extract_uml_code(response)  # Extract PlantUML code only
        print(uml_code)
        return uml_code
    except Exception as e:
        print("Error during UML generation:", e)
        return None

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



# # Example usage

# pdf_path = "inventory.pdf"
# uml_code = generate_uml_code(pdf_path)

# if uml_code:
#     with open("uml_data_output.txt", "w") as output_file:
#         output_file.write(uml_code)
#     print("UML code saved to uml_output.txt")


