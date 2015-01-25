import matplotlib.pyplot as plt

from searchengine.evaluation.evaluation import *

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
