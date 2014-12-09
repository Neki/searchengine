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
    with open(path) as f:
        return _build_cacm_documents(f)

class InvalidCacmDocument(Exception):

    def __init__(self, pos, *args, **kwargs):
        super()
        self.pos = pos


class ReachedEndOfFile(Exception):
    pass


# TODO : document reader that tracks whether or not we are at the end of file,
# to avoid having to use this nasty ReachedEndOfFile (which is really a
# glorified goto)
# it could be a generator (as to allow stream processing) !

def _build_cacm_documents(f):
    out = []
    while True:
        try:
            doc = _build_cacm_document(f)
            out.append(doc)
            print(doc.keywords)
        except ReachedEndOfFile as e:
            print(e)
            return out


def _build_cacm_document(f):
    doc_id = _read_document_id(f)
    title = None
    keywords = None
    abstract = None
    while True:
        try:
            next_field_type = _get_next_field_type(f)
            if next_field_type == FieldType.title:
                title = _read_field_data(f)
            elif next_field_type == FieldType.abstract:
                abstract = _read_field_data(f)
            elif next_field_type == FieldType.keywords:
                keywords = _read_field_data(f)
            elif next_field_type == FieldType.doc_id:  # go to next document
                return Document(doc_id, title, abstract, keywords)
        except ReachedEndOfFile:
            return Document(doc_id, title, abstract, keywords)


def _read_document_id(f):
    first_line = f.readline()
    if first_line is '':
        raise ReachedEndOfFile("End of file reached when reading next document id.")
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
        raise ReachedEndOfFile("End of file reached when trying to read next field")
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



