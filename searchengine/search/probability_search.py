from searchengine.index.process import InvertedIndex
from searchengine.parser import RequestDocument


def binary_independance_retrieval(request, document_list, common_words, nb_answers):
    request_doc = RequestDocument(request)
    request_index = InvertedIndex(common_words, [request_doc])
    index = InvertedIndex(common_words, document_list)
    out = []
    for doc_id in index.doc_ids:
        rsv = index.probability_rsv(request_index, doc_id)
        if rsv is not None:
            out.append((doc_id, rsv))
    return sorted(out, key=lambda x: -x[1])[:nb_answers]
