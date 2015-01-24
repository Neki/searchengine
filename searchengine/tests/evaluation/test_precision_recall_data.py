import unittest
from unittest import TestCase
from searchengine.evaluation.precision_recall_data import *
from searchengine.search.vectorial_search import vectorial_search
from searchengine.parser import CacmDocument
from searchengine.index.index import Weighting

class TestEvaluation(TestCase):

    def test_compute_interpolation(self):
        data = PrecisionRecallData([(0,1), (0.2, 0.7), (0.5, 0.4), (0.7, 0.2)])
        self.assertEqual(data.points, data.interpolated_points)
        data = PrecisionRecallData([(0,1), (0, 0), (0.2, 0.7), (0.2, 0.4), (0.6, 0.2), (0.7, 0.3)])
        self.assertEqual([(0, 1), (0.2, 0.7), (0.6, 0.3), (0.7, 0.3)], data.interpolated_points)

    def test_precision_for(self):
        data = PrecisionRecallData([(0,1), (0, 0), (0.2, 0.7), (0.2, 0.4), (0.6, 0.2), (0.7, 0.3)])
        self.assertEqual([(0, 1), (0.2, 0.7), (0.6, 0.3), (0.7, 0.3)], data.interpolated_points)
        self.assertEqual(1, data.precision_for(0))
        self.assertEqual(1, data.precision_for(0.1))
        self.assertEqual(0.3, data.precision_for(0.6))
        self.assertEqual(0.3, data.precision_for(0.65))
        self.assertEqual(0.7, data.precision_for(0.5))