import unittest
from unittest import TestCase
from searchengine.evaluation.average import *
from searchengine.evaluation.evaluation import Request

class TestAverage(TestCase):

    def test_compute_average_precision(self):
        requests = [Request(1, "tata", [1, 2, 3]), Request(2, "toto", [3, 4])]
        search_results = {1: [(2, 2), (3, 1)], 2: [(4, 1)]}
        avg_precision = compute_avg_precision(requests, search_results, [0, 0.5, 1], 3)
        self.assertEqual([0, 0.5, 1], [p[0] for p in avg_precision])
        self.assertEquals((0, 1), avg_precision[0])
