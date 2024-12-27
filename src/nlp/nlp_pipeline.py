import spacy
from keybert import KeyBERT

nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()
def process_text(text):
    
    doc = nlp(text)
    
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=10)
    
    return {
        "entities": entities,
        "noun_phrases": noun_phrases,
        "keywords": [kw for kw, _ in keywords]
    }
    
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


