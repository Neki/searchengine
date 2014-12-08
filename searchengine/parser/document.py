from enum import Enum


class Document:

    def __init__(self, doc_id, title, abstract, keywords):
        self.doc_id = doc_id
        self.title = title
        self.abstract = abstract
        self.keywords = keywords


class FieldType(Enum):
    doc_id = 1,
    title = 2,
    abstract = 3,
    publication_date = 4,
    authors = 5,
    added_date = 6,
    references = 7,
    keywords = 8


def load_from_cacm(path):
    out = []
    with open(path) as f:
        out.append(_build_cacm_document(f))
    return out


class InvalidCacmDocument(Exception):

    def __init__(self, line, *args, **kwargs):
        super(args, kwargs)
        self.line = line


def _build_cacm_document(f):
    doc_id = _read_document_id(f)
    next_field_type = _get_next_field_type(f)
    # TODO


def _read_document_id(f):
    first_line = f.readline()
    if not first_line.starts_with(".I"):
        raise InvalidCacmDocument(f.tell(), "First line of a document must start with .I")
    return first_line[2:].strip()


def _get_next_field_type(f):
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
    else:
        raise InvalidCacmDocument(f.tell(), "Unknown field type: {0}".format(type_id))


