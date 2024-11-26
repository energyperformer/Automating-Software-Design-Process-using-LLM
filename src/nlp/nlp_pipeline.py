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
    
