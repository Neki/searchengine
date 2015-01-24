import matplotlib.pyplot as plt
import bisect
import itertools


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


class PrecisionRecallData:

    def __init__(self, points): # TODO: document that
        if len(points) == 0:
            raise ValueError("A plot must have at least one point")
        self.__points = sorted(points, key=lambda x: x[0])
        self.__interpolated_points = self.__compute_interpolation(self.points)

    @property
    def points(self):
        return self.__points

    @property
    def interpolated_points(self):
        return self.__interpolated_points

    def __compute_interpolation(self, points):
        """
        Parameters:
            points (list of tuple of (int, int)): a list of points of (recall, precision)
        Returns:
            (list of tuple of (int, int)): the interpolated points. First point will always be (0, 1), and for a given recall value R, the associated precision will be the maximum precision encountered
            for recall values greater or equal than R.
        """

        # For a given recall value, only keep the greatest precision
        cleaned = []
        for k, g in itertools.groupby(points, lambda x: x[0]):
            cleaned.append(max(g, key=lambda x: x[1]))

        interpolated_points = [None] * len(cleaned)
        interpolated_points[-1] = points[-1]

        for i in range(len(cleaned) - 2, -1, -1):
            interpolated_points[i] = (cleaned[i][0], cleaned[i][1] if cleaned[i][1] > interpolated_points[i+1][1] else interpolated_points[i+1][1])

        interpolated_points[0] = (0, 1)
        return interpolated_points

    def precision_for(self, recall_level):
        """
        Parameters:
            recall_level (int): a recall value between 0 and 1
        Returns:
            (int) the corresponding interpolated precision value
        """
        # Binary search
        i = bisect.bisect_right([p[0] for p in self.__interpolated_points], recall_level)
        if i > 0:
            return self.__interpolated_points[i - 1][1]
        return self.__interpolated_points[0][1]


def compute_avg_precision(requests, search_results, recall_points, max_rank=100):
    """
    Parameters:
        request (list of Request)
        search_results (dict mapping int to list of tuple of (int, int)): a map between a request id and an ordonned list of returned documents id (together with their scores) for this request
        recalls (list of)
    Returns
        a list of tuples (recall, average precision over all the requests for this recall value)
    """
    #print(requests)
    #print(search_results)
    #print(recall_points)
    all_precisions = [list() for i in range(0, len(recall_points))]
    for request in requests:
        results = search_results[request.id]
        precisions = [precision(request, results[:rank]) for rank in range(0, 1 + min(len(search_results), max_rank))]
        recalls = [recall(request, results[:rank]) for rank in range(0, 1 + min(len(search_results), max_rank))]
        points = list(zip(recalls, precisions))
        #print(points)
        data = PrecisionRecallData(points)
        for i, r in enumerate(recall_points):
            all_precisions[i].append(data.precision_for(r))
    ys = [sum(l)/len(l) for l in all_precisions]
    assert len(recall_points) == len(ys)
    assert ys[0] == 1
    return list(zip(recall_points, ys))


def plot_avg_precision(requests, search_results, max_rank=100):
    """
    Parameters:
        request (list of Request)
        search_results (dict mapping int to tuple of (int, int)): a map between a request id, and an ordonned list of returned documents id (together with their scores) for this request
    """
    recalls = [x / 10 for x in range(0, 11)]
    points = compute_avg_precision(requests, search_results, recalls)
    xs = [p[0] * 100 for p in points]
    ys = [p[1] * 100 for p in points]

    # Plot
    fig, ax1 = plt.subplots()
    plt.axis([-5, 105, -5, 105])
    plt.xlabel('Rappel')
    plt.ylabel('Precision')
    plt.title('Evaluation')
    plt.plot(xs, ys, "o")
    plt.show()
