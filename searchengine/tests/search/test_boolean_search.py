from unittest import TestCase
from searchengine.search.boolean_search import WordNode, build_tree, tokenize_request, MismatchedParens, add_missing_ands, InvalidRequest, boolean_search
from searchengine.index.process import Index
from searchengine.parser.cacm_document import CacmDocument


class TestBooleanSearch(TestCase):

    def test_word_eval(self):
        document = CacmDocument(1, "common title", "not so common abstract", "unusual keywords")
        document2 = CacmDocument(2, "common title", "not so common abstract", "goal")
        index = Index(["common", "not", "so"], [document, document2])
        word_node = WordNode(index, "goal")
        self.assertCountEqual([2], word_node.eval())

    def test_build_tree(self):
        # Test that requests are parsed without errors
        index = None
        requests = ["a b or c", "a and (b or c)", "c and ((b or c) or (a and (c and d)))", "a and (b c)", "not a", "b and (not c)", "b and not c", "not (a or c)"]
        for request in requests:
            build_tree(request, index)
        # Test that badly formed requests are rejected
        requests = ["a (and b or c", "a (and b) or c", "a or b and c )"]
        for request in requests:
            self.assertRaises(MismatchedParens, build_tree, request, index)
        requests = ["and not c", "a or", "not or c", "b not c"]
        for request in requests:
            self.assertRaises(InvalidRequest, build_tree, request, index)

    def test_tokenize_request(self):
        request = "toto and (tata or not titi)"
        self.assertEqual(["toto", "and", "(", "tata", "or", "not",  "titi", ")"], tokenize_request(request))

    def test_add_missing_ands(self):
        base = ["toto", "or", "(", "tata", "titi", ")", "tutu"]
        expected = ["toto", "or", "(", "tata", "and", "titi", ")", "and", "tutu"]
        self.assertEqual(expected, add_missing_ands(base))

    def test_boolean_search(self):
        document = CacmDocument(1, "common title", "not so common abstract", "unusual keywords")
        document2 = CacmDocument(2, "common title", "not so common abstract", "target")
        document3 = CacmDocument(3, "my common title", "some abstract here", "goal")
        document_list = [document, document2, document3]
        common_words = ["common", "no", "so"]
        request = "(not common and goal) or target"
        self.assertCountEqual([3, 2], boolean_search(request, document_list, common_words))
        request = "((common and goal) or target) and not here"
        self.assertCountEqual([2], boolean_search(request, document_list, []))
        request = "title common"
        self.assertCountEqual([1, 2, 3], boolean_search(request, document_list, []))



