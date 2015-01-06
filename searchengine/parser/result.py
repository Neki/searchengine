from enum import Enum
from searchengine.evaluation.evaluation import Request
        
class InvalidRequest(Exception):

    def __init__(self, pos, *args, **kwargs):
        super()
        self.pos = pos


def load_from_results_file(path):
    """
    Parameter:
        path (string) - path to the CACM collection file
    Yields:
        Each document in the collection
    Example:
        >>> for document in load_from_cacm("/ressources/cacm.all"):
        >>>    process(document)
    """
    with open(path) as f:
        return load_from_results(f)

def load_from_results(f):
    """
    Similar to load_from_cacm, excepts that it takes a file object as a
    parameter instead of a path.
    """
    out = {}
    eof = False
    while not eof:
        eof, request_id, doc_id = _get_next_result(f)
        out[request_id] = doc_id
        #if request_id in out.keys():
        #    out[request_id] = out[request_id] + doc_id
        #else:
        #    out[request_id] = doc_id
    return out

def _get_next_result(f):
    request_id, doc_id = _read_request(f)
    while True:
        next_field_type = f.readline().strip()
        if next_field_type == '':  # end of file:
            return True, request_id, doc_id
        else:
            return False, request_id, doc_id

            
def _read_request(f):
    first_line = f.readline()
    print(first_line)
    if first_line.strip == '':
        raise InvalidRequest(f.tell(), "Unknown field type: {0}".format(type_id))
    return int(first_line[:2]),int(first_line[3:7])