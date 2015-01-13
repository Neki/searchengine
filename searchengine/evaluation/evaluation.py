import string
from searchengine.search.vectorial_search import vectorial_search
import matplotlib.pyplot as plt

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
    if max_rank is None:
        max_rank = len(search_results)
    fig, ax1 = plt.subplots()
    plt.axis([-5, 105, -5, 105])
    plt.xlabel('Rappel')
    plt.ylabel('Precision')
    plt.title('Evaluation')
    precisions = [precision(request, search_results[:rank]) for rank in range(0, min(len(search_results), max_rank))]
    recalls = [recall(request, search_results[:rank]) for rank in range(0, min(len(search_results), max_rank))]
    points = list(zip(recalls, precisions))
    interpolated_points = _interpolate_precision(points, max_rank)
    xs = [p[0] * 100 for p in interpolated_points]
    ys = [p[1] * 100 for p in interpolated_points]
    plt.plot(xs, ys, "o")
    plt.show()

def _interpolate_precision(points, max_rank):
    """
    Parameters:
        points (list of tuple of (int, int)): a list of points of (recall, precision)
    Returns:
        (list of tuple of (int, int)): the interpolated points. First point will always be (0, 1), and for a given recall value R, the associated precision will be the maximum precision encountered
        for recall values greater or equal than R.
    """
    interpolated_points = [None] * len(points)
    interpolated_points[-1] = points[-1]

    for i in range(len(points) - 2, -1, -1):
        interpolated_points[i] = (points[i][0], points[i][1] if points[i][1] > interpolated_points[i+1][1] else interpolated_points[i+1][1])

    out = []
    for i in range(0, len(interpolated_points) - 1):
        if interpolated_points[i][0] != interpolated_points[i+1][0]:
            out.append(interpolated_points[i])
    out.append(interpolated_points[-1])
    out[0] = (0, 1)
    return out


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
        yaxis2.append(recall(request, search_results[:rank])*100)
    ax2.plot(range(1,len(search_results)), yaxis2, 'b-')
    plt.show()
