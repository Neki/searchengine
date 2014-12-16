from unittest import TestCase
from searchengine.index.process import *
from searchengine.parser import CacmDocument


class TestUtils(TestCase):

    def test_tokenize(self):
        self.assertEqual(["aujourd", "hui", "lundi", "il", "fait", "beau", "enfin", "presque"], tokenize("aujourd'hui (lundi) il fait beau - enfin, presque."))
        self.assertEqual([], tokenize(""))

    def test_normalize(self):
        self.assertEqual("abcdef", normalize("AbCdEf"))
        self.assertEqual("abcdef", normalize("abcdef"))

    def test_remove_stop_words(self):
        self.assertEqual(["toto", "tata", "tyty"], remove_stop_words(["toto",
            "tata", "titi", "tutu", "tyty"], ["titi", "tutu"]))

    def test_statistics(self):
        self.assertEqual({"toto":3,"tata":2,"tyty":1}, count_occurences(["toto", "tata", "tyty", "toto", "toto", "tata"]).frequency)

    def test_get_word_list(self):
        document = CacmDocument(2382,"aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        self.assertEqual(["aujourd", "toto", "tata","il", "fait", "tyty","toto","tata","tyty"],get_word_list(document))

    def test_document_size(self):
        document = CacmDocument(2382,"aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        self.assertEqual(9, document_size(document))

    def test_document_statistics(self):
        document = CacmDocument(2382,"aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        common_words = ["aujourd","il","fait","ca","mot","ok"]
        self.assertEqual({"toto":2,"tata":2,"tyty":2}, document_word_count(document, common_words).frequency)


class TestIndex(TestCase):

    def test_add_document(self):
        document = CacmDocument(2, "title", "abstract", "keywords")
        index = InvertedIndex([])
        index.add_document(document)
        self.assertCountEqual(["title", "abstract", "keywords"], index.words)
        self.assertCountEqual([2], index.doc_ids)

        document2 = CacmDocument(3, "title2", "abstract", "keywords")
        index.add_document(document2)
        self.assertCountEqual(["title", "title2", "abstract", "keywords"], index.words)
        self.assertCountEqual([2, 3], index.doc_ids)

    def test_no_repetition(self):
        document = CacmDocument(2, "title", "abstract", "keywords")
        index = InvertedIndex([], [document])
        self.assertRaises(ValueError, index.add_document, document)

    def test_weights(self):
        document = CacmDocument(2, "title title", "abstract", "keywords")
        index = InvertedIndex([], [document])
        weights = index.get_weights(2)
        self.assertEqual(0.5, weights["title"])
        self.assertEqual(0.25, weights["abstract"])

    def test_common_words(self):
        document = CacmDocument(2, "common title", "not so common abstract", "unusual keywords")
        index = InvertedIndex(["common", "not", "so"], [document])
        self.assertCountEqual(["title", "abstract", "unusual", "keywords"], index.words)


class TestDocStats(TestCase):

    def test_weights(self):
        stats = DocStats({"toto": 20, "tata": 50}, 100)
        self.assertEqual(0.2, stats.weights["toto"])
        self.assertEqual(0.5, stats.weights["tata"])









