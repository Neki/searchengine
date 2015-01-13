import unittest
from unittest import TestCase
from searchengine.evaluation.evaluation import *
from searchengine.search.vectorial_search import vectorial_search
from searchengine.parser import CacmDocument
from searchengine.index.process import Weighting

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

    def test_interpolation(self):
        data = PrecisionRecallData([(0,1), (0.2, 0.7), (0.5, 0.4), (0.7, 0.2)])
        self.assertEqual(data.points, data.interpolated_points)
        data = PrecisionRecallData([(0,1), (0, 0), (0.2, 0.7), (0.2, 0.4), (0.6, 0.2), (0.7, 0.3)])
        self.assertEqual([(0, 1), (0.2, 0.7), (0.6, 0.3), (0.7, 0.3)], data.interpolated_points)
        self.assertEqual(1, data.precision_for(0))
        self.assertEqual(1, data.precision_for(0.1))
        self.assertEqual(0.3, data.precision_for(0.6))
        self.assertEqual(0.3, data.precision_for(0.65))
        self.assertEqual(0.7, data.precision_for(0.5))

    def test_average_precision(self):
        requests = [Request(1, "tata", [1, 2, 3]), Request(2, "toto", [3, 4])]
        search_results = {1: [(2, 2), (3, 1)], 2: [(4, 1)]}
        avg_precision = compute_avg_precision(requests, search_results, [0, 0.5, 1])
        self.assertEqual([0, 0.5, 1], [p[0] for p in avg_precision])
        self.assertEquals((0, 1), avg_precision[0])

    @unittest.skip("Skipping until Travis CI is properly configured (this test blocks otherwise)")
    def test_plot_precision_recall(self):
        request = Request(1,"tata",[1,2])
        document1 = CacmDocument(1, "aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        document2 = CacmDocument(2,"plouf \n paf","tata \n toto il tata","tyty plouf \n tata paf")
        document_list = [document1, document2]
        common_words=["aujourd","il","fait","ca","mot","ok"]
        search_results = vectorial_search(request.text, document_list, common_words, 2,Weighting.TermFrequency)
        plot_precision_vs_recall(request, search_results)
