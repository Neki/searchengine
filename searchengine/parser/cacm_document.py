from enum import Enum


class CacmDocument:

    def __init__(self, doc_id, title, abstract, keywords):
        self.doc_id = doc_id
        self.title = title
        self.abstract = abstract
        self.keywords = keywords

    def get_full_text(self):
        """
        Returns:
            a string containing the title, abstract and keywords (each field is separated by a newline)
        """
        out = ""
        for s in [self.title, self.abstract, self.keywords]:
            if s is not None:
                out += s
                out += "\n"
        return out


class FieldType(Enum):
    doc_id = 1,
    title = 2,
    abstract = 3,
    publication_date = 4,
    authors = 5,
    added_date = 6,
    references = 7,
    keywords = 8


class InvalidCacmDocument(Exception):

    def __init__(self, pos, *args, **kwargs):
        super()
        self.pos = pos


def load_from_cacm_file(path):
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
        yield from load_from_cacm(f)


def load_from_cacm(f):
    """
    Similar to load_from_cacm, excepts that it takes a file object as a
    parameter instead of a path.
    """
    eof = False
    while not eof:
        eof, doc = _get_next_cacm_document(f)
        yield doc


def _get_next_cacm_document(f):
    doc_id = _read_document_id(f)
    title = None
    keywords = None
    abstract = None
    while True:
        next_field_type = _get_next_field_type(f)
        if next_field_type == FieldType.title:
            title = _read_field_data(f)
        elif next_field_type == FieldType.abstract:
            abstract = _read_field_data(f)
        elif next_field_type == FieldType.keywords:
            keywords = _read_field_data(f)
        elif next_field_type is None:  # end of file
            return True, CacmDocument(doc_id, title, abstract, keywords)
        elif next_field_type == FieldType.doc_id:  # go to next document
            return False, CacmDocument(doc_id, title, abstract, keywords)
        else:
            _ = _read_field_data(f)


def _read_document_id(f):
    first_line = f.readline()
    if not _is_beginning_document_(first_line):
        raise InvalidCacmDocument(f.tell(), "First line of a document must"
                                    " start with .I, got {0}".format(first_line))
    return int(first_line[2:].strip())


def _get_next_field_type(f):
    last_pos = f.tell()
    type_id = f.readline().strip()
    if type_id == ".T":
        return FieldType.title
    elif type_id == ".W":
        return FieldType.abstract
    elif type_id == ".B":
        return FieldType.publication_date
    elif type_id == ".A":
        return FieldType.authors
    elif type_id == ".N":
        return FieldType.added_date
    elif type_id == ".X":
        return FieldType.references
    elif type_id == ".K":
        return FieldType.keywords
    elif _is_beginning_document_(type_id):
        f.seek(last_pos)
        return FieldType.doc_id
    elif type_id == '':  # end of file:
        return None
    else:
        raise InvalidCacmDocument(f.tell(), "Unknown field type: {0}".format(type_id))


def _is_field_declarator(line):
    type_id = line.strip()
    return type_id in [".T", ".W", ".A", ".N", ".X", ".K", ".B"]


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



