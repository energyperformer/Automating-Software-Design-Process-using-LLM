import PyPDF2
# import spacy
# from keybert import KeyBERT
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# import torch
# import os
# from graphviz import Graph

# nlp = spacy.load("en_core_web_sm")
# kw_model = KeyBERT()

# model_name = "gpt2"
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)

# GRAPHVIZ_PATH = r"C:\Program Files\Graphviz\bin"

def process_srs_document(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


# def extract_key_information(text):
#     doc = nlp(text)
    
#     actors = [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG"]]
    
#     use_cases = [chunk.text for chunk in doc.noun_chunks if chunk.root.pos_ == "VERB"]
    
#     keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=10)
    
#     return {
#         "actors": actors,
#         "use_cases": use_cases,
#         "keywords": [kw for kw, _ in keywords]
#     }

# def process_text(text):
#     return extract_key_information(text)

# def generate_uml_code(extracted_info):
#     prompt = f"""
#     Generate PlantUML code for a use case diagram with the following information:
#     Actors: {', '.join(extracted_info['actors'])}
#     Use Cases: {', '.join(extracted_info['use_cases'])}
#     Keywords: {', '.join(extracted_info['keywords'])}
#     """
    
#     input_ids = tokenizer.encode(prompt, return_tensors="pt")
#     output = model.generate(input_ids, max_length=500, num_return_sequences=1, temperature=0.7)
    
#     uml_code = tokenizer.decode(output[0], skip_special_tokens=True)
#     return uml_code

# def render_uml_diagram(uml_code, output_path):
#     try:
#         dot = Graph(comment='Use Case Diagram', format='png', engine='dot')
#         dot.attr(rankdir='LR')

#         lines = uml_code.split('\n')
#         actors = []
#         use_cases = []
        
#         for line in lines:
#             if line.startswith('actor'):
#                 actor = line.split('"')[1]
#                 actors.append(actor)
#                 dot.node(actor, actor, shape='ellipse')
#             elif line.startswith('usecase'):
#                 use_case = line.split('"')[1]
#                 use_cases.append(use_case)
#                 dot.node(use_case, use_case, shape='rectangle')
#             elif '-->' in line:
#                 source, target = line.split('-->')
#                 source = source.strip().strip('"')
#                 target = target.strip().strip('"')
#                 dot.edge(source, target)

#         dot.engine = os.path.join(GRAPHVIZ_PATH, 'dot')

#         dot.render(output_path, view=False, cleanup=True)
#         print(f"UML diagram generated and saved to {output_path}.png")
#         return True
#     except Exception as e:
#         print(f"Unexpected error generating UML diagram: {e}")
#         return False

# __all__ = ['generate_uml_code']
