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
        self.assertEqual(1, index.nb_documents)

        document2 = CacmDocument(3, "title2", "abstract", "keywords")
        index.add_document(document2)
        self.assertCountEqual(["title", "title2", "abstract", "keywords"], index.words)
        self.assertCountEqual([2, 3], index.doc_ids)
        self.assertEqual(2, index.nb_documents)

    def test_no_repetition(self):
        document = CacmDocument(2, "title", "abstract", "keywords")
        index = InvertedIndex([], [document])
        self.assertRaises(ValueError, index.add_document, document)

    def test_weights(self):
        document = CacmDocument(2, "title title", "abstract", "keywords")
        index = InvertedIndex([], [document])
        weights = index.get_weights(2)
        self.assertEqual(2, weights["title"])
        self.assertEqual(1, weights["abstract"])

    def test_common_words(self):
        document = CacmDocument(2, "common title", "not so common abstract", "unusual keywords")
        index = InvertedIndex(["common", "not", "so"], [document])
        self.assertCountEqual(["title", "abstract", "unusual", "keywords"], index.words)

    def test_word_count(self):
        document = CacmDocument(1, "title", "abstract abstract", "keywords")
        document2 = CacmDocument(2, "title", "abstract", "keywords")
        index = InvertedIndex([], [document, document2])
        self.assertEqual(3, index.get_word_count("abstract"))

    def test_word_list(self):
        document = CacmDocument(1, "title", "abstract abstract", "keywords")
        document2 = CacmDocument(2, "title", "abstract", "keywords")
        document3 = CacmDocument(3, "title", "notanabstract", "keywords")
        index = InvertedIndex([], [document, document2, document3])
        self.assertCountEqual([1, 2], index.get_doc_ids_containing("abstract"))

    def test_nb_documents_with_word(self):
        document = CacmDocument(1, "title", "abstract abstract", "keywords")
        document2 = CacmDocument(2, "title", "abstract", "keywords")
        document3 = CacmDocument(3, "title", "summary", "keywords")
        index = InvertedIndex([], [document, document2, document3])
        self.assertEqual(2, index.get_nb_docs_with_word("abstract"))


class TestDocStats(TestCase):

    def test_frequency_weights(self):
        stats = DocStats({"toto": 20, "tata": 50}, 100)
        self.assertEqual(20, stats.weights()["toto"])
        self.assertEqual(50, stats.weights()["tata"])

    def test_log_frequency_weights(self):
        stats = DocStats({"toto": 20, "tata": 50}, 100)
        self.assertGreaterEqual(0.001, abs(2.301 - stats.weights(weighting=Weighting.LogTermFrequency)["toto"]))
        self.assertGreaterEqual(0.001, abs(2.699 - stats.weights(weighting=Weighting.LogTermFrequency)["tata"]))

    @unittest.skip("Test not written yet")
    def test_tf_idf(self):
        pass



class TestTermInfo(TestCase):

    def test_word_count(self):
        info = TermInfo()
        info.add_document(1, 23)
        info.add_document(1, 2)
        self.assertEqual(25, info.count)
