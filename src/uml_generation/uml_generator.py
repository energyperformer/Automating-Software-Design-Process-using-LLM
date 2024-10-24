# from transformers import T5ForConditionalGeneration, RobertaTokenizer


# model_name = "Salesforce/codet5-small"  # You can choose other sizes like base, large, etc.
# tokenizer = RobertaTokenizer.from_pretrained(model_name)
# model = T5ForConditionalGeneration.from_pretrained(model_name)


# def generate_use_case_uml(processed_data):
#     entities = processed_data.get('entities', [])
#     noun_phrases = processed_data.get('noun_phrases', [])
    
#     # Extract potential actors and use cases
#     actors = list(set([ent[0] for ent in entities if ent[1] in ['PERSON', 'ORG']]))[:5]  # Limit to 5 actors
#     use_cases = list(set([np for np in noun_phrases if np.lower().startswith(('manage', 'create', 'update', 'delete', 'view', 'process', 'generate', 'analyze'))][:10]))  # Limit to 10 use cases
    
#     # Use CodeT5 to generate UML code
#     input_text = f"Generate UML for actors: {', '.join(actors)} and use cases: {', '.join(use_cases)}"
#     input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    
#     outputs = model.generate(input_ids, max_length=500, num_return_sequences=1)
#     generated_uml = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
#     # Post-process the generated UML code
#     uml_code = "@startuml\n"
    
#     # Add actors
#     for actor in actors:
#         actor = actor.replace('"', '').replace('\n', ' ').strip()  # Remove quotes and newlines
#         if actor:
#             uml_code += f'actor "{actor}"\n'
    
#     # Add use cases
#     for use_case in use_cases:
#         use_case = use_case.replace('"', '').replace('\n', ' ').strip()  # Remove quotes and newlines
#         if use_case:
#             uml_code += f'usecase "{use_case}"\n'
    
#     # Add some connections
#     for i, actor in enumerate(actors):
#         actor = actor.replace('"', '').replace('\n', ' ').strip()
#         for j in range(min(2, len(use_cases))):
#             use_case = use_cases[j].replace('"', '').replace('\n', ' ').strip()
#             if actor and use_case:
#                 uml_code += f'"{actor}" --> "{use_case}"\n'
    
#     # Append any additional generated UML code
#     uml_code += generated_uml
    
#     uml_code += "\n@enduml"
#     return uml_code

# def generate_uml_code(processed_data):
#     return generate_use_case_uml(processed_data)

# __all__ = ['generate_uml_code']
from transformers import T5ForConditionalGeneration, RobertaTokenizer

model_name = "Salesforce/codet5-small"  # You can choose other sizes like base, large, etc.
tokenizer = RobertaTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate_use_case_uml(processed_data):
    entities = processed_data.get('entities', [])
    noun_phrases = processed_data.get('noun_phrases', [])
    
    # Extract potential actors and use cases
    actors = list(set([ent[0] for ent in entities if ent[1] in ['PERSON', 'ORG']]))[:5]  # Limit to 5 actors
    use_cases = list(set([np for np in noun_phrases if np.lower().startswith(('manage', 'create', 'update', 'delete', 'view', 'process', 'generate', 'analyze'))][:10]))  # Limit to 10 use cases
    
    # Use CodeT5 to generate UML code
    input_text = f"Generate UML for actors: {', '.join(actors)} and use cases: {', '.join(use_cases)}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    
    outputs = model.generate(input_ids, max_length=500, num_return_sequences=1)
    generated_uml = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Post-process the generated UML code
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
    
    # Add connections
    for actor in actors:
        actor = actor.replace('"', '').replace('\n', ' ').strip()
        for use_case in use_cases[:2]:  # Connect each actor to up to 2 use cases
            use_case = use_case.replace('"', '').replace('\n', ' ').strip()
            if actor and use_case:
                uml_code += f'"{actor}" --> "{use_case}"\n'
    
    # Append any additional generated UML code, ensuring no syntax errors
    generated_lines = generated_uml.split('\n')
    for line in generated_lines:
        if line.strip() and not line.strip().startswith('@') and not line.strip().endswith(')'):
            uml_code += line.strip() + '\n'
    
    uml_code += "@enduml"
    return uml_code

def generate_uml_code(processed_data):
    return generate_use_case_uml(processed_data)

__all__ = ['generate_uml_code']