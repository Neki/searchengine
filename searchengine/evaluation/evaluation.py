import string
from searchengine.search.vectorial_search import vectorial_search

class Request:

    def __init__(self, id, text, result):
        self.id = id
        self.text = text
        self.result = result # list of doc ids

def number_of_relevant_documents(request, search_result):
    out = 0
    for doc_id in request.result:
        for res in search_result:
            if doc_id == res[0]:
                out = out+1
    return out

def precision(request, document_list, common_words, rank):
    """ 
    Number of relevant documents found on number of found documents
    """
    search_result = vectorial_search(request.text, document_list, common_words, rank)
    return number_of_relevant_documents(request, search_result)/rank
    
def rappel(request, document_list, common_words, rank):
    """ 
    Number of relevant documents found on number of relevant documents
    """
    search_result = vectorial_search(request.text, document_list, common_words, rank)
    return number_of_relevant_documents(request, search_result)/len(request.result)

