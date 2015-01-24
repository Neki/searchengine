import unittest
from unittest import TestCase
from searchengine.evaluation.evaluation import *
from searchengine.search.vectorial_search import vectorial_search
from searchengine.parser import CacmDocument
from searchengine.index.index import Weighting

class TestEvaluation(TestCase):

    def test_number_of_relevant_documents(self):
        request = Request(1, "tata", [1, 2, 5, 12])
        search_result = [(1, 20), (2, 3), (4, 5), (7, 2)]
        self.assertEqual(2, number_of_relevant_documents(request, search_result))

    def test_precision(self):
        request = Request(1, "tata", [1, 2, 5, 12])
        search_result = [(1, 20), (2, 3), (4, 5), (7, 2)]
        self.assertEqual(0.5, precision(request, search_result))
        self.assertEqual(1, precision(request, []))

    def test_recall(self):
        request = Request(1, "tata", [1, 2, 3, 4, 5, 6, 7, 8])
        search_result = [(1, 20), (3, 3), (42, 42)]
        self.assertEqual(0.25, recall(request, search_result))
        request2 = Request(2, "tata", [])
        self.assertEqual(0, recall(request2, search_result))

    @unittest.skip("Skipping until Travis CI is properly configured (this test blocks otherwise)")
    def test_plot_precision_recall(self):
        request = Request(1,"tata",[1,2])
        document1 = CacmDocument(1, "aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        document2 = CacmDocument(2,"plouf \n paf","tata \n toto il tata","tyty plouf \n tata paf")
        document_list = [document1, document2]
        common_words=["aujourd","il","fait","ca","mot","ok"]
        search_results = vectorial_search(request.text, document_list, common_words, 2,Weighting.TermFrequency)
        plot_precision_vs_recall(request, search_results)
