# import spacy
# import en_core_web_sm

import spacy
from keybert import KeyBERT

nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

def extract_key_information(text):
    doc = nlp(text)
    
    # Extract potential actors (named entities that are persons or organizations)
    actors = [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG"]]
    
    # Extract potential use cases (verb phrases)
    use_cases = [chunk.text for chunk in doc.noun_chunks if chunk.root.pos_ == "VERB"]
    
    # Extract keywords
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=10)
    
    return {
        "actors": actors,
        "use_cases": use_cases,
        "keywords": [kw for kw, _ in keywords]
    }

# try:
#     nlp = spacy.load("en_core_web_sm")
# except IOError:
#     print("Downloading spaCy model...")
#     spacy.cli.download("en_core_web_sm")
#     nlp = spacy.load("en_core_web_sm")

# def process_text(text):
#     try:
#         doc = nlp(text[:1000000])  # Limit text to 1 million characters to avoid memory issues
        
#         entities = [(ent.text, ent.label_) for ent in doc.ents]
#         noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        
#         return {
#             "entities": entities,
#             "noun_phrases": noun_phrases
#         }
#     except Exception as e:
#         print(f"Error in NLP processing: {str(e)}")
#         return {
#             "entities": [],
#             "noun_phrases": []
#         }

def process_text(text):
    doc = nlp(text)
    
    # Extract entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Extract noun phrases
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    
    # Extract keywords
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=10)
    
    return {
        "entities": entities,
        "noun_phrases": noun_phrases,
        "keywords": [kw for kw, _ in keywords]
    }
