from searchengine.index.index import Index
from math import sqrt
from searchengine.parser import RequestDocument


def vectorial_search(request, index, nb_answers, weighting_method):
    """
    Parameters : a request, documents list, common words, number of answers and weighting method
    Result : a list of k document ids ranked by pertinence
    """
    out = []  # list of pairs (doc_id, pertinence)
    request_doc = RequestDocument(request)
    request_index = Index(index.common_words, [request_doc])
    request_weights = request_index.get_weights(request_doc.doc_id, weighting_method, index)
    for doc_id in index.doc_ids:
        doc_weights = index.get_weights(doc_id, weighting_method, index)
        l1, l2 = build_weights_vectors(request_weights, doc_weights)
        sim = similarity(l1, l2)
        if sim != 0:
            out.append((doc_id, sim))
    out = sorted(out, key=lambda x: -x[1])
    return out[:nb_answers]


def similarity(l1, l2):
    """
    Returns the similarity between l1 and l2
    """
    assert(len(l1) == len(l2))
    assert(len(l1) > 0)
    scalar = 0
    for i in range(0, len(l1)):
        scalar += l1[i] * l2[i]
    if scalar == 0:
        return 0
    norm1 = sqrt(sum(v ** 2 for v in l1))
    norm2 = sqrt(sum(v ** 2 for v in l2))
    return scalar / (norm1 * norm2)


def build_weights_vectors(weights1, weights2):
    """
    Parameters:
        weights1, weights2: dictionnaries mapping words to their weight
    Returns:
        two lists (vectors) in the space where each word is an axis
    Example:
        >>> w1 = {"word":2, "hey":1, "nope":3}
        >>> w2 = {"word":1, "nope": 4}
        >>> l1, l2 = build_weights_vectors(w1, w2)
        >>> print(l1)
        [2, 1, 3]
        >>> print(l2):
        [1, 0, 4]
    """
    l1 = []
    l2 = []
    for word in set(weights1.keys()) | set(weights2.keys()):
        if word in weights1.keys():
            l1.append(weights1[word])
        else:
            l1.append(0)
        if word in weights2:
            l2.append(weights2[word])
        else:
            l2.append(0)
    return l1, l2
