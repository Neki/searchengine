import matplotlib.pyplot as plt
import bisect
import itertools

from searchengine.evaluation.precision_recall_data import *

class Request:
    """
    A request together with a list of expected relevant documents (identified by doc_id)
    """
    def __init__(self, id, text, result):
        self.id = id
        self.text = text
        self.result = result # list of doc ids

def number_of_relevant_documents(request, search_results):
    """
    Parameters:
        request (Request)
        search_results (list of tuples): a list of tuples (doc_id, score)
    Returns:
        (int) the number of relevant documents (according to a known request) in a set of documents
    """
    out = 0
    for doc_id in request.result:
        for res in search_results:
            if doc_id == res[0]:
                out = out+1
    return out

def precision(request, search_results):
    """
    Number of relevant documents found in `search_results` over total number of documents.
    """
    if len(search_results) == 0:
        return 1
    return number_of_relevant_documents(request, search_results)/len(search_results)

def recall(request, search_results):
    """
    Number of relevant documents found over total number of relevant documents in the collection.
    """
    if len(request.result) == 0:
        return 0
    return number_of_relevant_documents(request, search_results)/len(request.result)

def plot_precision_vs_recall(request, search_results, max_rank=None):
    """
    Parameters: a request, its search results and a rank
    Displays a graph with recall as abscissa and precision as ordinate
    """
    if max_rank is None:
        max_rank = len(search_results)
    fig, ax1 = plt.subplots()
    plt.axis([-5, 105, -5, 105])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Evaluation')
    precisions = [precision(request, search_results[:rank]) for rank in range(0, min(len(search_results), max_rank))]
    recalls = [recall(request, search_results[:rank]) for rank in range(0, min(len(search_results), max_rank))]
    points = list(zip(recalls, precisions))
    data = PrecisionRecallData(points)
    interpolated_points = data.interpolated_points
    xs = [p[0] * 100 for p in interpolated_points]
    ys = [p[1] * 100 for p in interpolated_points]
    plt.plot(xs, ys, "o")
    plt.show()