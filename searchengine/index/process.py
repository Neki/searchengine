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
    return [word for word in word_list if word not in common_words]
