import json
from transformers import pipeline

def load_knowledge_base(base_path):
    """
    Loads a knowledge base for retrieval.
    """
    with open(base_path, 'r') as file:
        return json.load(file)

def retrieve_relevant_knowledge(query, knowledge_base):
    """
    Retrieves relevant knowledge from a knowledge base using semantic search.
    """
    retriever = pipeline("question-answering")
    results = []
    for item in knowledge_base:
        context = item['context']
        answer = retriever(question=query, context=context)
        results.append((answer['score'], context))
    results.sort(reverse=True)
    return results[:3]  # Top 3 results
