import string
from searchengine.search.vectorial_search import vectorial_search
import matplotlib.pyplot as plt

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

def plot_precision_rappel(request, document_list, common_words):
    fig, ax1 = plt.subplots()
    plt.axis([0, len(document_list), 0, 100])
    plt.xlabel('Rank')
    ax1.set_ylabel('Precision', color='r')
    plt.title('Evaluation')
    yaxis = []
    for rank in range(1,len(document_list)):
        yaxis.append(precision(request, document_list, common_words, rank)*100)
    ax1.plot(range(1,len(document_list)), yaxis, 'ro')
        
    ax2 = ax1.twinx()
    plt.axis([0, len(document_list), 0, 100])
    ax2.set_ylabel('Rappel', color='b')
    plt.title('Evaluation')
    yaxis2 = []
    for rank in range(1,len(document_list)):
        yaxis2.append(rappel(request, document_list, common_words, rank)*100)
    ax2.plot(range(1,len(document_list)), yaxis2, 'bo')
    plt.show()
