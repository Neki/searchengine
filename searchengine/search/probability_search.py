from searchengine.index.process import Index
from searchengine.parser import RequestDocument


def binary_independance_retrieval(request, document_list, common_words, nb_answers):
    """
    Parameters: request, list of documents, common words and number of answers required
    Result : a sorted list of k document ids ranked by pertinence
    """
    request_doc = RequestDocument(request)
    request_index = Index(common_words, [request_doc])
    index = Index(common_words, document_list)
    out = []
    for doc_id in index.doc_ids:
        rsv = index.probability_rsv(request_index, doc_id)
        if rsv is not None:
            out.append((doc_id, rsv))
    return sorted(out, key=lambda x: -x[1])[:nb_answers]
