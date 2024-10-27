from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2"  
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)


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

def generate_uml_code(processed_data):
    return generate_use_case_uml(processed_data)

__all__ = ['generate_uml_code']    
  