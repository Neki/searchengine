from searchengine.index.process import InvertedIndex
from searchengine.parser import RequestDocument

class Tree:
    def __init__(self):
        self.__nodes = {}
    
    @property
    def nodes(self):
        return self.__nodes
    
    def add_node(self, identifier, parent=None):
        node = Node(identifier)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)

        return node   
    
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
        return 
    else:
        return False
    
def build_tree(request):
    operators=["and","or", "not"]
    t = Node()
    p = []
    r = request.split(" ")
    for c in r:
        if c in "([{":
            p.append(t)
            t.children[0] = Node()
            t = t.children[0]
        elif c in operators:
            if c in ["and", "or"]:
                rac = top(pi)
                p = pop(p)
                rac.rac = c
                rac.children[0] = t
                p.append(rac)
                rac.children[1] = Node()
                t = rac.children[1]
                
            else:
                rac = top(pi)
                p = pop(p)
                rac.rac = c
                rac.children[0] = Node()
                p.append(rac)
                rac.children[1] = Node()
                t = rac.children[1]
        elif c in ")]}":
            rac = top(pi)
            p = pop(p)
            rac.children[1] = t
            t = rac
        else:
            t = Node()
    if length(p) == 0:
        return t
    else:
        raise "Not well parenthesized"
            
def boolean_search(request, document_list, common_words):
    tree = build_tree(request)
    pass
