import string
from searchengine.search.vectorial_search import vectorial_search
import matplotlib.pyplot as plt

class Request:

    def __init__(self, id, text, result):
        self.id = id
        self.text = text
        self.result = result # list of doc ids

def number_of_relevant_documents(request, search_results):
    out = 0
    for doc_id in request.result:
        for res in search_results:
            if doc_id == res[0]:
                out = out+1
    return out

def precision(request, search_results):
    """ 
    Number of relevant documents found over number of found documents
    """
    print("relevant docs found = "+str(number_of_relevant_documents(request, search_results)))
    print("docs found = " + str(len(search_results)))
    return number_of_relevant_documents(request, search_results)/len(search_results)
    
def rappel(request, search_results):
    """ 
    Number of relevant documents found over number of relevant documents
    """
    return number_of_relevant_documents(request, search_results)/len(request.result)

def courbe_rappel_precision(request, search_results):
    fig, ax1 = plt.subplots()
    plt.axis([0, 100, 0, 100])
    plt.xlabel('Rappel')
    plt.ylabel('Precision')
    plt.title('Evaluation')
    xaxis = []
    yaxis = []
    for rank in range(1,len(search_results)):
        xaxis.append(precision(request, search_results[:rank])*100)
        yaxis.append(rappel(request, search_results[:rank])*100)
        print(" rappel x = " + str(xaxis[len(xaxis)-1])+"\n")
    plt.plot(xaxis, yaxis)
    plt.show()

def plot_precision_rappel(request, search_results):
    fig, ax1 = plt.subplots()
    plt.axis([0, len(search_results), 0, 100])
    plt.xlabel('Rank')
    ax1.set_ylabel('Precision', color='r')
    plt.title('Evaluation')
    yaxis = []
    for rank in range(1,len(search_results)):
        yaxis.append(precision(request, search_results[:rank])*100)
    ax1.plot(range(1,len(search_results)), yaxis, '-r')
        
    ax2 = ax1.twinx()
    plt.axis([0, len(search_results), 0, 100])
    ax2.set_ylabel('Rappel', color='b')
    plt.title('Evaluation')
    yaxis2 = []
    for rank in range(1,len(search_results)):
        yaxis2.append(rappel(request, search_results[:rank])*100)
    ax2.plot(range(1,len(search_results)), yaxis2, 'b-')
    plt.show()
