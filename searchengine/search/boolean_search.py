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
            
def parser(request):
    pass

def boolean_search(request, document_list, common_words):
    pass
