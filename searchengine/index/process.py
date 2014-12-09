import string


def tokenize(line):
    cleaned = ''.join([_punctuation_to_space(c) for c in list(line)])
    tokens = [token for token in cleaned.split(" ") if token not in string.whitespace]
    return tokens


def _punctuation_to_space(character):
    separators = string.punctuation
    if character in separators:
        return " "
    return character

def normalize(term):
    return term.lower()

def remove_stop_words(word_list, common_words):
    return [normalize(word) for word in word_list if word not in common_words]

def statistics(word_list):
    out = {}
    for word in word_list:
        if word not in out.keys():
            out[word] = 1
        else:
             out[word] = out[word] +1
    return out

def get_word_list(document):
    word_list = []
    for line in document.title.split("\n"):
        word_list = word_list + tokenize(line)
    for line in document.abstract.split("\n"):
        word_list = word_list + tokenize(line)
    for line in document.keywords.split("\n"):
        word_list = word_list + tokenize(line)
    return word_list

def document_statistics(document, common_words):
    word_list = get_word_list(document)
    return statistics(remove_stop_words(word_list,common_words))

def inverted_index(document_list, common_words, word):
    out = {}
    stats = {}
    for doc_id in document_list.keys():
        stats[doc_id] = document_statistics(document_list[doc_id], common_words)
        if word in stats[doc_id].keys():
            out[doc_id] = stats[doc_id][word]
    return out
