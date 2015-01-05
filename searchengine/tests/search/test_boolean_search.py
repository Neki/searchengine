from unittest import TestCase
from searchengine.search.boolean_search import WordNode, build_tree, tokenize_request, MismatchedParens, add_missing_ands
from searchengine.index.process import InvertedIndex
from searchengine.parser.cacm_document import CacmDocument


class TestBooleanSearch(TestCase):

    def test_eval(self):
        document = CacmDocument(2, "common title", "not so common abstract", "unusual keywords")
        index = InvertedIndex(["common", "not", "so"], [document])
        word_node = WordNode(index, "goal")
        self.assertGreaterEqual(False, word_node.eval(2))

    def test_build_tree(self):
        # Test that requests are parsed without errors
        index = None
        requests = ["a b or c", "a and (b or c)", "c and ((b or c) or (a and (c and d)))", "a and (b c)"]
        for request in requests:
            build_tree(request, index)
        # Test that badly formed requests are rejected
        requests = ["a (and b or c", "a (and b) or c", "a or b and c )"]
        for request in requests:
            self.assertRaises(MismatchedParens, build_tree, request, index)

    def test_tokenize_request(self):
        request = "toto and (tata or not titi)"
        self.assertEqual(["toto", "and", "(", "tata", "or", "not",  "titi", ")"], tokenize_request(request))

    def test_add_missing_ands(self):
        base = ["toto", "or", "(", "tata", "titi", ")", "tutu"]
        expected = ["toto", "or", "(", "tata", "and", "titi", ")", "and", "tutu"]
        self.assertEqual(expected, add_missing_ands(base))




