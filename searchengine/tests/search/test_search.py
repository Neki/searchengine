from unittest import TestCase
from searchengine.search.vectorial_search import similarity, build_weights_vectors


class TestSearch(TestCase):

    def test_similarity(self):
        l1 = [1, 2, 3]
        l2 = [2, 3, 4]
        self.assertGreaterEqual(0.00001, abs(0.99258 - similarity(l1, l2)))

    def test_build_weights_vectors(self):
        w1 = {"word": 2, "hey": 1, "nope": 3}
        w2 = {"word": 1, "nope": 4, "yo": 5}
        l1, l2 = build_weights_vectors(w1, w2)
        self.assertCountEqual([2, 1, 3, 0], l1)
        self.assertCountEqual([1, 0, 4, 5], l2)
        word_index = l1.index(2)
        hey_index = l1.index(1)
        nope_index = l1.index(3)
        self.assertEqual(l2[word_index], 1)
        self.assertEqual(l2[hey_index], 0)
        self.assertEqual(l2[nope_index], 4)
