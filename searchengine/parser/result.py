from enum import Enum
from searchengine.evaluation.evaluation import Request

class InvalidRequest(Exception):

    def __init__(self, pos, *args, **kwargs):
        super()
        self.pos = pos


def load_from_results_file(path):
    """
    Parameter:
        path (string) - path to the CACM results file
    Returns:
        A list of all result documents
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
        if request_id in out.keys():
            out[request_id].append(doc_id)
        else:
            out[request_id] = [doc_id]
    return out

def _get_next_result(f):
    request_id, doc_id = _read_result(f)
    while True:
        if is_next_result_empty(f):  # end of file:
            return True, request_id, doc_id
        else:
            return False, request_id, doc_id

def is_next_result_empty(f):
    last_pos = f.tell()
    next_field_type = f.readline().strip()
    f.seek(last_pos)
    return next_field_type == ''

def _read_result(f):
    first_line = f.readline()
    if first_line.strip() == '':
        raise InvalidRequest(f.tell(), "empty result")
    return int(first_line[:2]),int(first_line[3:7])

