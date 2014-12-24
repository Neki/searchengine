from searchengine.index.process import InvertedIndex
from searchengine.parser import RequestDocument
    
class Node:
    def __init__(self, *children):
        self._children = children

    @property
    def children(self):
        return self.__children
    
class AndNode:
    def __init__(self,left,right):
        super().__init__(left,right)
        
    def eval(self):
        for child in self._children:
            if not child.eval():
                return False
        return True
    
class OrNode:
    def __init__(self,left,right):
        super().__init__(left,right)
    
    def eval(self):
        for child in self._children:
            if child.eval():
                return True
        return False
    
class NotNode:
     def __init__(self, right):
        super().__init__(right)    
        
     def eval(self):
        assert(size(self._children)==1)
        return not self._children[0].eval()
        
class WordNode:
    def __init__(self,index, word):
        self.index = index
        self.word = word
        
    def eval(self, doc_id):
        return self.word in self.index.get_words_by_doc_id(doc_id)
            
def is_well_parenthesized(request):
    pile = []
    for c in request:
        if c in "([{":
            pile.append(c)
        elif c in ")]}":
            if length(pile) == 0:
                return False
            else:
                temp = top(pile)
                pile = pop(pile)
                if c!=temp:
                    return False
    if length(pile) == 0:
        return true
    else:
        return False

def tokenize_request(request):
    cleaned = ''.join([_punctuation_to_space(c) for c in list(line)])
    tokens = [token for token in cleaned.split(" ") if token not in string.whitespace]
    return tokens

def _punctuation_to_space(character):
    separators = string.punctuation
    for c in "{[(])}":
        separators.replace(c,"")
    if character in separators:
        return " "
    return character
    
def build_tree(request):
    operators=["and","or", "not"]
    t = WordNode({},"")
    p = []
    r = tokenize_request(request)
    for c in r:
        if c in "([{":
            p.append(t)
            t.children[0] = WordNode({},"")
            t = t.children[0]
        elif c in operators:
            if c in ["and", "or"]:
                rac = top(pi)
                p = pop(p)
                rac.rac = c
                rac.children[0] = t
                p.append(rac)
                rac.children[1] = WordNode({},"")
                t = rac.children[1]
            else:
                rac = top(pi)
                p = pop(p)
                rac.rac = c
                rac.children[0] = WordNode({},"")
                p.append(rac)
                rac.children[1] = WordNode({},"")
                t = rac.children[1]
        elif c in ")]}":
            rac = top(pi)
            p = pop(p)
            rac.children[1] = t
            t = rac
        else:
            t = WordNode({},"")
    if length(p) == 0:
        return t
    else:
        raise "Not well parenthesized"
            
def boolean_search(request, document_list, common_words):
    #for doc in document_list: 
    #    return tree.eval(doc)
    pass
