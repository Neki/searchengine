from enum import Enum
from searchengine.evaluation.evaluation import Request

class FieldType(Enum):
    id = 1,
    text = 2,
    rest = 3,
    author = 4

class InvalidRequest(Exception):

    def __init__(self, pos, *args, **kwargs):
        super()
        self.pos = pos


def load_from_query_file(path):
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
        return load_from_query(f)


def load_from_query(f):
    """
    Similar to load_from_cacm, excepts that it takes a file object as a
    parameter instead of a path.
    """
    out = {}
    eof = False
    while not eof:
        eof, id, text = _get_next_request(f)
        out[id] = text
    return out

def _get_next_request(f):
    id = _read_request_id(f)
    while True:
        next_field_type = _get_next_field_type(f)
        if next_field_type == FieldType.text:
            text = _read_field_data(f)
        elif next_field_type is None:  # end of file
            return True, id, text
        elif next_field_type == FieldType.id:  # go to next request
            return False, id, text
        else:
            _ = _read_field_data(f)


def _read_request_id(f):
    first_line = f.readline()
    if not _is_beginning_document_(first_line):
        raise InvalidRequest(f.tell(), "First line of a request must"
                                    " start with .I, got {0}".format(first_line))
    return int(first_line[2:].strip())


def _get_next_field_type(f):
    last_pos = f.tell()
    type_id = f.readline().strip()
    if type_id == ".I":
        return FieldType.id
    elif type_id == ".W":
        return FieldType.text
    elif type_id == ".N":
        return FieldType.rest
    elif type_id == ".A":
        return FieldType.author
    elif _is_beginning_document_(type_id):
        f.seek(last_pos)
        return FieldType.id
    elif type_id == '':  # end of file:
        return None
    else:
        raise InvalidRequest(f.tell(), "Unknown field type: {0}".format(type_id))


def _is_field_declarator(line):
    type_id = line.strip()
    return type_id in [".I", ".W",".N",".A"]


def _is_beginning_document_(line):
    return line.strip().startswith(".I")


def _read_field_data(f):
    out = []
    last_pos = f.tell()

    while True:
        last_pos = f.tell()
        line = f.readline()
        if line != '' and not _is_field_declarator(line) and not _is_beginning_document_(line):
            out.append(line)
        else:
            f.seek(last_pos)
            break

    return "\n".join(out)
