from unittest import TestCase
from searchengine.search.boolean_search import *
from searchengine.parser.cacm_document import CacmDocument

class TestBooleanSearch(TestCase):
    
    def test_eval(self):
        document = CacmDocument(2, "common title", "not so common abstract", "unusual keywords")
        index = InvertedIndex(["common", "not", "so"], [document])
        word_node = WordNode(index,"goal")
        self.assertGreaterEqual(False,word_node.eval(2))

