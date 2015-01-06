import string
import re
from searchengine.index.process import InvertedIndex


class Node:
    def __init__(self, *children):
        self._children = children

    @property
    def children(self):
        return self.__children


class AndNode(Node):
    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        return self._children[0].eval() & self._children[1].eval()

    def __repr__(self):
        return "AndNode( ({0}) and ({1}) )".format(self._children[0], self._children[1])


class OrNode(Node):
    def __init__(self, left, right):
        super().__init__(left, right)

    def eval(self):
        return self._children[0].eval() | self._children[1].eval()

    def __repr__(self):
        return "OrNode( ({0}) or ({1}) )".format(self._children[0], self._children[1])


class NotNode(Node):
    def __init__(self, right, index):
        super().__init__(right)
        self.index = index

    def eval(self):
        assert(len(self._children) == 1)
        return set(self.index.doc_ids) - self._children[0].eval()

    def __repr__(self):
        return "NotNode( not {0} )".format(self._children[0])


class WordNode(Node):
    def __init__(self, index, word):
        self.index = index
        self.word = word

    def eval(self):
        return set(self.index.get_doc_ids_containing(self.word))

    def __repr__(self):
        return "WordNode( {0} )".format(self.word)


def tokenize_request(request):
    """
    Example:
       >>> tokenize_request("a and b,c or (d and e)")
       ["a", "and", "b", "c", "or", "(", "d", "and", "e", ")"]
    """
    return [t for t in re.split('(\W)', request) if t == "(" or t == ")" or not (t in string.whitespace or t in string.punctuation)]


def build_tree(request, index):
    """
    Build a request boolean tree from a request.
    Parameters:
        request (str): a request ("a and (b or c)")
        index (InvertedIndex)
    Returns:
        (Node) the root node of the request tree
    """
    tokens = tokenize_request(request)
    tokens = add_missing_ands(tokens)
    #print("------- processing request {0}".format(request))
    return tokens_to_node(tokens, index)


def add_missing_ands(tokens):
    """
    Parameter:
        tokens (list of str)
    Returns:
        (list of str)
    Example:
        >>> add_missing_ands(["a", "b", "(","a", "b",")", "e"])
        ["a", "and", "b", "and", "(", "a", "and", "b", ")", "and", "e"]
    """
    out = []
    for i in range(0, len(tokens) - 1):
        a = tokens[i]
        b = tokens[i+1]
        out.append(a)
        if (is_word(a) and is_word(b)) or (a == ")" and is_word(b)) or (is_word(a) and b == "("):
            out.append("and")
    out.append(tokens[-1])
    return out


def is_word(token):
    return token not in ["and", "or", "not", ")", "("]


class MismatchedParens(Exception):
    pass


class InvalidRequest(Exception):
    pass


def tokens_to_node(tokens, index):
    """
    Transforms a list of tokens into a boolean tree. Respects operator precedence and parenthesis.
    Parameters:
        tokens (list of str)
        index (InvertedIndex)
    Returns:
        Node
    """
    # the implementation is an adaptation of the shunting-yard algorithm
    # instead of building the output stack in pstfix form and then having another pass
    # to build the tree from the output stack, the tree is computed while the tokens are read
    stack = []  # a stack of (pending) operators
    output = []  # a stack containing nodes or the separator "("
                 # at the end of the algorithm, this stack will contain only the root of the tree
    operators = {"and": 2, "or": 1, "not": 3}  # boolean operators with their precedence
    for token in tokens:
        #print("token: {0} / output: {1} / stack: {2}".format(token, output, stack))
        if token in operators:
            if len(stack) == 0:
                stack.append(token)
            else:
                top = stack[-1]
                while(top in operators and operators[top] > operators[token]):
                    top = stack.pop()
                    _build_node(top, index, stack, output)
                    if len(stack) == 0:
                        break
                    top = stack[-1]
                stack.append(token)
        elif token == "(":
            stack.append(token)
            output.append("(")
        elif token == ")":
            if len(stack) == 0:
                raise MismatchedParens
            top = stack.pop()
            while top != "(":
                if len(stack) == 0:
                    raise MismatchedParens
                _build_node(top, index, stack, output)
                top = stack.pop()
            assert(len(output) >= 2)
            top = output.pop()
            paren = output.pop()
            if paren != "(":
                raise MismatchedParens
            output.append(top)
        else:  # the token is a word
            output.append(WordNode(index, token))
    #print("no more tokens")
    while(len(stack) > 0):
        #print("output: {0} / stack: {1}".format(output, stack))
        top = stack.pop()
        if top == "(" or top == ")":
            raise MismatchedParens
        _build_node(top, index, stack, output)
    if len(output) > 1:
        raise InvalidRequest
    return output[0]


# Used inside the above method
def _build_node(node_type, index, stack, output):
    assert node_type in ["and", "or", "not"]
    if node_type == "not":
        if len(output) == 0:
            raise InvalidRequest("Not enough variables provided for operator 'not'")
        output.append(NotNode(output.pop(), index))
        return
    if len(output) < 2:
        raise InvalidRequest("Not enough variables provided for operator {0}".format(node_type))
    left = output.pop()
    if left == "(":
        raise MismatchedParens
    right = output.pop()
    if right == "(":
        raise MismatchedParens
    if node_type == "and":
        output.append(AndNode(left, right))
    elif node_type == "or":
        output.append(OrNode(left, right))
    #print("applied operator: output : {0} / stack : {1}".format(output, stack))


def boolean_search(request, document_list, common_words, answer_count=None):
    index = InvertedIndex(common_words, document_list)
    request_tree = build_tree(request, index)
    return request_tree.eval()


