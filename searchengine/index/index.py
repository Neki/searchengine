import string
import math
from enum import Enum


class Weighting(Enum):
    TermFrequency = 1,
    LogTermFrequency = 2,
    Tf_Idf = 3


class Index:
    def __init__(self, common_words, documents=None):
        self.__index = {}  # a dict mapping words to TermInfo
        self.__stats = {}  # a dict mapping doc IDs to DocStats
        self.common_words = common_words
        self.__nb_documents = 0
        if documents is not None:
            for doc in documents:
                self.add_document(doc)

    def get_words_by_doc_id(self, doc_id):
        return self.__stats[doc_id].frequency.keys()

    def add_document(self, document):
        """
        Parameters:
            document : a document (must respond to `doc_id` and `get_full_text`).

            Document IDs must be unique in the index.
        Raises:
            ValueError: when trying to insert a document whose ID already exists in the index
        """
        stats = document_word_count(document, self.common_words)
        if document.doc_id in self.__stats:
            raise ValueError("Document ID {0} is already present in this index".format(document.doc_id))
        for word, count in stats.frequency.items():
            assert(count > 0)
            if word not in self.__index:
                self.__index[word] = TermInfo()
            self.__index[word].add_document(document.doc_id, count)
        self.__stats[document.doc_id] = stats
        self.__nb_documents += 1

    def get_word_count(self, word):
        """
        Returns:
            the number of occurences of the given word in the collection
        """
        if word in self.__index:
            return self.__index[word].count
        return 0

    def get_nb_docs_with_word(self, word):
        if word not in self.__index:
            return 0
        return self.__index[word].nb_documents

    @property
    def words(self):
        """
        Returns:
            list of str: the words in this index dictionnary (e.g. the indexed keywords)
        """
        return self.__index.keys()

    @property
    def doc_ids(self):
        """
        Returns:
            list of int: a list of the IDs of the documents indexed in this index
        """
        return self.__stats.keys()

    def get_weights(self, doc_id, weighting_method, corpus_index=None):
        """
        Parameter:
            doc_id (int): a document ID. This document must be present in the index.
            weighting_method (Weighting): the method used to compute the weight of each term in the document
            corpus_index (Index): used only for the method Tf_Idf, the index for the corpus (not of the request). This parameter is ignored for other weighting methods.
        Returns:
            A dict mapping the words in the given document to their weights.
        """
        return self.__stats[doc_id].weights(weighting_method, corpus_index)

    @property
    def nb_documents(self):
        return self.__nb_documents

    def get_doc_ids_containing(self, word):
        """
        Parameter:
            word (str)
        Returns:
            list of int: a list of the IDs of documents containing the word (may be empty)
        """
        if word not in self.__index:
            return []
        return self.__index[word].docs.keys()

    def probability_rsv(self, request_index, doc_id):
        """
        Parameters:
            request_index (Index)
            doc_id (int)
        Returns:
          (float) The retrieval status value for the document (relative to the given request), under the PRP (probability ranking principe) model and the BIR (binary independance retrieval) hypothesis
        """
        intersect = set(request_index.words) & set(self.__stats[doc_id].words)
        if len(intersect) == 0:
            return None
        rsv = 0
        for word in intersect:
            dft = self.get_nb_docs_with_word(word)
            assert(dft >= 1)  # dft >= 1 by definition of intersect
            a = math.log10(self.nb_documents / dft)
            pr = 0.5  # TODO: use a more sophisticated method
            b = math.log10(pr / (1 - pr))
            rsv += b + a
        return rsv


class TermInfo:
    """Various statistics about a word (relative to the entire collection)
    """
    def __init__(self):
        self.docs = {} # doc_id, freq
        self.count = 0

    def add_document(self, doc_id, count):
        if doc_id in self.docs:
            self.docs[doc_id] += count
        else:
            self.docs[doc_id] = count
        self.count += count

    @property
    def nb_documents(self):
        return len(self.docs)


class DocStats:
    """Various statistics about a document.
    """

    def __init__(self, frequency, nb_words):
        """
        Parameters:
            frequency (dict): a dictionary mapping words to their number of occurences
            nb_words (int): the number of words in the document.
        """
        self.frequency = frequency
        self.nb_words = nb_words

    def weights(self, weighting, index=None):
        """
        Returns:
            a dictionary mapping each word in the document to a weight
        """
        if weighting == Weighting.TermFrequency:
            return self.__term_frequency_weights()
        elif weighting == Weighting.LogTermFrequency:
            return self.__log_term_frequency_weights()
        elif weighting == Weighting.Tf_Idf:
            if index is None:
                raise ValueError("An index must be provided to compute the tf-idf weights")
            return  self.__tf_idf_weights(index)
        else:
            raise ValueError("Unsupported weighting method: {0}".format(weighting))

    @property
    def words(self):
        return self.frequency.keys()

    def __term_frequency_weights(self):
        """
        Returns:
            a dictionary mapping each word in the document to a tf weight
        """
        out = {}
        for word in self.frequency.keys():
            out[word] = self.frequency[word]
        # Normalization
        return {word: frequency / max(out.values()) for word, frequency in out.items()}

    def __log_term_frequency_weights(self):
        """
        Returns:
            a dictionary mapping each word in the document to a ltf weight
        """
        out = {}
        for word in self.frequency.keys():
            if self.frequency[word] > 0:
                out[word] = 1 + math.log10(self.frequency[word])
        # Normalization
        return {word: weight / max(out.values()) for word, weight in out.items()}

    def __tf_idf_weights(self, index):
        """
        Returns:
            a dictionary mapping each word in the document to a tf-idf weight
        """
        out = {}
        for word in self.frequency.keys():
            dft = index.get_nb_docs_with_word(word)
            if self.frequency[word] > 0 and dft > 0:
                out[word] = (1 + math.log10(self.frequency[word])) * math.log10(index.nb_documents / dft)
        # Normalization
        return {word: weight / max(out.values()) for word, weight in out.items()}



def document_word_count(document, common_words):
    """
    Parameters:
        document (Document)
        common_words (list of str)
    Returns:
        A dictionnary:
        - keys: words inside the `document`, except the `common_words`
        - values: number of occurences of the word in the `document`
    Example:
        >>> document = CacmDocument(2382,"aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        >>> common_words= ["aujourd", "il", "fait", "ca", "mot", "ok"]
        >>> document_statistics(document,common_words)
        { "toto":2, "tata":2, "tyty":2 }
    """
    word_list = get_word_list(document)
    return count_occurences(remove_stop_words(word_list, common_words))


def count_occurences(word_list):
    """
    Parameter:
        word_list (list of str)
    Returns:
        A dictionnary:
        - keys : each word in the `word_list`
        - values : number of occurences of the word in the `word_list`
    Example:
        >>> statistics(["toto", "tata", "tyty", "toto", "toto", "tata"]) == DocStats({"toto":3,"tata":2,"tyty":1},9)
        True
    """
    out = {}
    for word in word_list:
        if word not in out.keys():
            out[word] = 1
        else:
            out[word] = out[word] + 1
    return DocStats(out, len(word_list))


def _punctuation_to_space(character):
    """
    Parameter:
        character (char)
    Returns:
        char: a space if `character` was a punctuation character, `character` otherwise
    Example:
        >>> _punctuation_to_space("-") == " "
        True
    """
    separators = string.punctuation
    if character in separators:
        return " "
    return character


def tokenize(line):
    """
    Parameter:
        line (str)
    Returns:
        a list a words without ponctuation or spaces
    Example:
        >>> tokenize("aujourd'hui (lundi) il fait beau -")
        ["aujourd", "hui", "lundi", "il", "fait", "beau"]
    """
    cleaned = ''.join([_punctuation_to_space(c) for c in list(line)])
    tokens = [token for token in cleaned.split(" ") if token not in string.whitespace]
    return tokens
def normalize(term):
    """
    Parameter:
        term (str)
    Returns:
        string: `term` converted to lowercase
    Example:
        >>> normalize("tEsT")
        test
    """
    return term.lower()


def remove_stop_words(word_list, common_words):
    """
    Parameters:
        word_list (list of str)
        common_words (list of str)
    Returns:
        list of str: all the words in `word_list` that do not belong to `common_words`
    Example:
        remove_stop_words([tata", "titi"], ["titi"]) returns ["tata"]
    """
    return [normalize(word) for word in word_list if word not in common_words]


def get_word_list(document):
    """
    Parameter:
        document (CacmDocument)
    Returns:
        list of str: all the words inside a document, without the punctation
    Example:
        >>> get_word_list(document) returns ["aujourd", "toto", "tata","il", "fait", "tyty","toto","tata","tyty"] == CacmDocument(2382,"aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        True
    """
    word_list = []
    for line in document.get_full_text().split("\n"):
        word_list = word_list + tokenize(line)
    return word_list


def document_size(document):
    """
    Parameter:
        document (Document)
    Returns:
        int: the number of words in the document
    Example:
        >>> document_size(CacmDocument(2382,"aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty"))
        9
    """
    size = 0
    for word in get_word_list(document):
        size = size + 1
    return size
