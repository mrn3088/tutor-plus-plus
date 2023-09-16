from langchain.vectorstores import FAISS
from langchain.schema import Document


def search_coarse(question, db):
    results_with_scores = db.similarity_search_with_score(question)
    
    for doc, score in results_with_scores:
        return doc.page_content, doc.metadata, score
    
def search_fine(question, db, filter):
    results_with_scores = db.similarity_search_with_score(question, filter=filter)
    
    for doc, score in results_with_scores:
        return doc.page_content, doc.metadata, score